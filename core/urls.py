from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home_page"),
    path('admin-login',admin_login,name='admin'),
    path('jobportal-admin',dashboard,name='jobportal-dashboard'),
    path('admin_home/',admin_home,name="admindashboard"),
    path('statistics',statistics,name="statistics"),
]