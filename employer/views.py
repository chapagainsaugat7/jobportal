from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from .models import Employer
from django.contrib.auth.hashers import make_password,check_password

import logging

logger = logging.getLogger(__name__)
# Create your views here.




def register_employer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        normalized_email = email.lower();
        hashed_password = make_password(password)
        

        ''' 
            check if email or phone number exists or not.
        '''
        email_exists = Employer.objects.filter(emp_email = normalized_email).exists()
        phone_exists = Employer.objects.filter(emp_phone_number = number).exists()

        message = ''
        if email_exists:
            message = "Email is taken."

        if phone_exists:
            message = "Phone number is taken."

        
        if email_exists or phone_exists:
            messages.error(request,message) 
            return render(request,'forms/employer.html')     

        else:
            pass
    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')

# R@ju_1234


def employer_dashboard(request):
    return render(request,'employer-dashboard/index.html')