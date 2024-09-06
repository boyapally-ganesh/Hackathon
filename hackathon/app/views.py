from django.shortcuts import render,HttpResponseRedirect
from rest_framework.response import Response 
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework import generics, permissions
from .models import*
from .serializers import HackathonSerializer, SubmissionSerializer, RegistrationSerializer


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny

# Register API
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "message": "User created successfully. Please log in."
        }, status=status.HTTP_201_CREATED)

# Login API
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)



class HackathonListCreateAPIView(generics.ListCreateAPIView):
    queryset = HackathonModels.objects.all()
    serializer_class = HackathonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Assign the logged-in user as the hackathon creator."""
        serializer.save(created_by=self.request.user)
        return HttpResponseRedirect('hackathons/')  # Redirect after form submission

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # After successfully creating the object, return a redirect or any success response
        return Response(response.data, status=status.HTTP_201_CREATED)


class RegisterForHackathonAPIView(generics.CreateAPIView):
    queryset = RegistrationModel.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        hackathon = HackathonModels.objects.get(id=kwargs.get('hackathon_id'))
        serializer = RegistrationSerializer(data=request.data, context={'request': request, 'hackathon': hackathon})
    
        serializer.is_valid(raise_exception=True)
        serializer.save()

    # Return the success message from the serializer
        return Response({"message": serializer.success_message}, status=status.HTTP_201_CREATED)


class SubmissionListAPIView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return submissions made by the logged-in user for hackathons they are enrolled in."""
        user = self.request.user
        return SubmissionModel.objects.filter(user=user)

    def get_serializer_context(self):
        """Add additional context if needed."""
        context = super().get_serializer_context()
        return context



class SubmissionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        """Add hackathon to serializer context."""
        context = super().get_serializer_context()
        hackathon_id = self.kwargs.get('hackathon_id')
        try:
            hackathon = HackathonModels.objects.get(id=hackathon_id)
        except HackathonModels.DoesNotExist:
            hackathon = None
        context['hackathon'] = hackathon
        return context

    def perform_create(self, serializer):
        """Create a new submission for a hackathon."""
        hackathon = self.get_serializer_context().get('hackathon')
        if hackathon is None:
            raise serializers.ValidationError("Hackathon not found.")
        serializer.save(hackathon=hackathon, user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new submission and return a success message.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request, 'hackathon': self.get_serializer_context().get('hackathon')})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Submission created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

class UserEnrolledHackathonsAPIView(generics.ListAPIView):
    serializer_class = HackathonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return hackathons the logged-in user is enrolled in."""
        user = self.request.user
        # Adjusted to use the correct related name
        enrolled_hackathons = HackathonModels.objects.filter(registrations__user=user)
        return enrolled_hackathons


