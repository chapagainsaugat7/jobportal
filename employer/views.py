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
            return JsonResponse({"message":"Email already exists."},status = 406)
        
        else:
            employer = Employer(emp_name = name,emp_phone_number = number,emp_email = normalized_email,emp_password = hashed_password)
            try:
                employer.save()
                return JsonResponse({"message":"Account Successfully created","email":normalized_email,"url":"employer_dashboard"},status=200)
            except Exception as e:
                return JsonResponse({"message":"Internal Server Error."},status = 500)

    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')

# R@ju_1234


def employer_dashboard(request):
    return render(request,'employer-dashboard/index.html')