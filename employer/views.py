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


        if Employer.objects.filter(emp_email = normalized_email):
            messages.error(request,"Email already exists.") 
            return render(request,'forms/employer.html')                
        elif Employer.objects.filter(emp_number = number):
            messages.error(request,"Phone number already exists.")
            return render(request,'forms/employer.html')
    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')

# R@ju_1234


def employer_dashboard(request):
    return render(request,'employer-dashboard/index.html')