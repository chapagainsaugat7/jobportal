from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home_page"),    
    path('portal-admin',admin,name='admin'),
    path('portal-test',admin_test,name='admin-test'),
    path('admin_home/',admin_home,name="admin_home")
]