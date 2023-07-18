from django.urls import path
from .views import *


urlpatterns = [
     path('register_job_seeker/',register_job_seeker,name='jobseeker_registration'),
    path('login/',login,name="login_form"),
   
]
