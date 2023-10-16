from django.urls import path
from .views import *
urlpatterns = [
    path('',jobseeker_dashboard,name="jobseeker-dashboard"),
    path('register-job-seeker/',register_job_seeker,name='register_jobseeker'),
    path('login/',login,name="login"),
    path('create-profile',create_profile,name="create-profile"),
    path('profile',profile,name="profile"),
    path('logout',logout_jobseeker,name='logout'),
    path('browsejob/<int:id>',browse_job,name="browsejob"),
    path('view_employer/<int:employer>',view_employer,name="view_employer"),
    path('downloadcv/<uuid:jobseeker_id>',download_cv,name="downloadcv"),
    path('applyjob/',applyjob,name='applyjob'),
]
