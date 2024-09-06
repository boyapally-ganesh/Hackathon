from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    # Hackathons
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('hackathons/', views.HackathonListCreateAPIView.as_view(), name='hackathon-list-create'),
    path('hackathons/<uuid:hackathon_id>/register/', views.RegisterForHackathonAPIView.as_view(), name='register-hackathon'),
    path('user/enrolled-hackathons/', views.UserEnrolledHackathonsAPIView.as_view(), name='user-enrolled-hackathons'),
    path('hackathons/submissions/', views.SubmissionListAPIView.as_view(), name='submission-list'),
    path('hackathons/<uuid:hackathon_id>/submissions/create/', views.SubmissionCreateAPIView.as_view(), name='submission-create'),
    
]

