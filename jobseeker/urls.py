from django.urls import path
from . import views

app_name = 'jobseeker'

urlpatterns = [
    path('', views.jobseeker_dashboard, name="job-seeker-dashboard"),
    path('register-job-seeker/', views.register_job_seeker, name='register-job-seeker'),
    path('login/', views.login, name="login"),
    path('jobseeker-dashboard', views.jobseeker_dashboard, name='dashboard'),
    path('create-profile', views.create_profile, name="create-profile"),
    path('profile', views.profile, name="profile"),
]
