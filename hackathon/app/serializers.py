from rest_framework import serializers
from .models import HackathonModels, SubmissionModel, RegistrationModel
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
class UserSerializer(serializers.ModelSerializer):
    """
    serializer for the user model to show basic user information.
    """
    class Meta:
        model = User
        fields = ['id','username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Both username and password are required")
        
        data['user'] = user
        return data



class HackathonSerializer(serializers.ModelSerializer):
    """
    Serializer for the HackathonModel
    """
    created_by = UserSerializer(read_only=True)
    submissions_count = serializers.SerializerMethodField()
    authorized = serializers.BooleanField(read_only=True)
    class Meta:
        model = HackathonModels
        fields = ['id','title','description','background_image','hackathon_image','submissions_type','start_datetime','end_dateTime','reward_prize','created_by','authorized','submissions_count']
        read_only_fields = ['created_by']
    def get_submissions_count(self, obj):
        """Returns the number of submissions for a hackathons"""
        return obj.submissions.count()
    
    def validate(self, data):
        """
        custom validation for hackathon cretion.
        """
        if data['end_dateTime'] < data['start_datetime']:
            raise serializers.ValidationError("End datetime cannot be earlier than start datetime.")
        return data
    def create(self, validated_data):
        """
        Attach the logged-in user as the creator of the hackathon.
        """
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)



class SubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for SubmissionModel.
    """
    user = UserSerializer(read_only=True)
    hackathon = HackathonSerializer(read_only=True)

    class Meta:
        model = SubmissionModel
        fields = [
            'id', 'hackathon', 'user', 'submission_name',
            'summary', 'submission_image', 'submission_file',
            'submission_link', 'created_at'
        ]

    def validate(self, data):
        """
        Custom Validation based on submission type.
        """
        hackathon = self.context.get('hackathon', None)
        if hackathon is None:
            raise serializers.ValidationError("Hackathon not found.")

        # Check if the user has already submitted to this hackathon
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            if SubmissionModel.objects.filter(user=request.user, hackathon=hackathon).exists():
                raise serializers.ValidationError("You have already submitted a submission for this hackathon.")

        # Ensure hackathon is not None before accessing its attributes
        if hackathon is None:
            raise serializers.ValidationError("Hackathon is not specified.")

        if hackathon.submissions_type == 'image' and not data.get('submission_image'):
            raise serializers.ValidationError("Image submission required.")
        if hackathon.submissions_type == 'file' and not data.get('submission_file'):
            raise serializers.ValidationError("File submission required.")
        if hackathon.submissions_type == 'link' and not data.get('submission_link'):
            raise serializers.ValidationError("Link submission required.")

        return data

    def create(self, validated_data):
        """
        Attach the logged-in user and hackathon to the submissions.
        """
        request = self.context.get('request', None)
        hackathon = self.context.get('hackathon', None)

        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
            validated_data['hackathon'] = hackathon

        return super().create(validated_data)




class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration to a hackathon.
    """
    user = UserSerializer(read_only=True)
    hackathon = HackathonSerializer(read_only=True)

    class Meta:
        model = RegistrationModel
        fields = ['id', 'user', 'hackathon', 'registered_at']
        read_only_fields = ['hackathon', 'user']

    def validate(self, attrs):
        """
        Ensure the user is not already registered for the hackathon.
        """
        request = self.context.get('request', None)
        hackathon = self.context.get('hackathon', None)

        # Check if the user is already registered
        if request and hackathon:
            if RegistrationModel.objects.filter(user=request.user, hackathon=hackathon).exists():
                raise ValidationError("You are already registered for this hackathon.")

        return attrs

    def create(self, validated_data):
        """
        Automatically attach the user and the selected hackathon, then display a success message.
        """
        request = self.context.get('request', None)
        hackathon = self.context.get('hackathon', None)  # Corrected typo

        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
            validated_data['hackathon'] = hackathon

        registration = super().create(validated_data)

        # You can add a custom attribute for success message
        self.success_message = "You have successfully registered for the hackathon."

        return registration


        

