from django.urls import path
from .views import *

urlpatterns = [
    path('register_employer/',register_employer,name='employer_registration'),
    path('login_employer/',employer_signin,name="employer_signin"),
]
