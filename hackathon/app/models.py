from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
# Create your models here.

class HackathonModels(models.Model):
    """
    Model to store information about a Hackathon.
    """

    SUBMISSION_TYPE = [
        ('image', 'image'),
        ('file', 'File'),
        ('link', 'Link')
    ]

    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    background_image = models.ImageField(upload_to="hackthons/backgrounds/", null=True, blank=True)
    hackathon_image = models.ImageField(upload_to='hackthons/', null=True, blank=True)
    submissions_type = models.CharField(max_length=10, choices =  SUBMISSION_TYPE)
    start_datetime = models.DateTimeField()
    end_dateTime = models.DateTimeField()
    reward_prize = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete= models.CASCADE)
    authorized = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_datetime']

class SubmissionModel(models.Model):
    """
    Model to store user submissions for a hackathon
    """
    id = models.UUIDField(default=uuid4, editable = False, primary_key = True)
    hackathon = models.ForeignKey(HackathonModels, related_name = 'submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name = 'submissions', on_delete=models.CASCADE)
    submission_name = models.CharField(max_length=255)
    summary = models.TextField()


    # store submission based on type
    submission_image = models.ImageField(upload_to='submissions/images/', null=True, blank=True)
    submission_file = models.FileField(upload_to='submission/files/', null=True, blank=True)
    submission_link = models.URLField(null=True, blank = True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Validate that only the correct submission type is provided based on the HackathonModel's submission type.

        """
        if self.hackathon.submission_type == 'image' and not self.submission_image:
            raise ValidationError('Image submission required.')
        
        if self.hackathon.submission_type == 'file' and not self.submission_file:
            raise ValidationError('file submission required.')
        if self.hackathon.submission_type == 'link' and not self.submission_link:
            raise ValidationError('link submission required.')
    def __str__(self):
        return f'Submission: {self.submission_name} by {self.user.username} for {self.hackathon.title}'

class RegistrationModel(models.Model):
    """
    Model to track user registration for hackathons.
    """    
    user = models.ForeignKey(User, related_name='registration', on_delete=models.CASCADE)
    hackathon = models.ForeignKey(HackathonModels, related_name='registrations', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} registered for {self.hackathon.title}'  