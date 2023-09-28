from django.urls import path
from .views import *

app_name = 'employer'

urlpatterns = [
    path('register_employer/', register_employer, name='registration'),
    path('login_employer/', employer_signin, name='signin'),
    path('employer_dashboard/', employer_dashboard, name='dashboard')
]
