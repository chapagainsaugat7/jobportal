from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home_page"),
    path('register_job_seeker/',register_job_seeker,name='jobseeker_registration'),
    path('login/',login,name="login_form"),
    path('login_employer',employer_signin,name="employer_signin"),
    path('register_employer/',register_employer,name='employer_registration'),

    path('portal-admin',admin,name='admin'),
    path('portal-test',admin_test,name='admin'),
    
]