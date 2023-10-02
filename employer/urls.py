from django.urls import path
from .views import *

urlpatterns = [
    path('register_employer/',register_employer,name='employer_registration'),
    path('login_employer/',employer_signin,name="employer_signin"),
    path('employer_dashboard/',employer_dashboard,name="employer_dashboard"),
    path('company_profile/',company_profile,name="company_profile")
]
