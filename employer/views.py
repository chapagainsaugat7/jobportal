from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from .models import Employer
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.




def register_employer(request):

    if request.method == 'POST':
        # name number email, type_of_hiring,password
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = make_password(password)
        # normaline email, 
        normalized_email = email.lower()

        if Employer.objects.filter(emp_email = normalized_email):
           return JsonResponse({"message":"Email is taken"},status=406)
        else:
            try:
                employer = Employer(emp_name = name,emp_phone_number = number,emp_email = normalized_email,emp_password = hashed_password)
                employer.save()
                return JsonResponse({"message":"Account Created."},status=200)
            except Exception as e:
                print(e)
                return JsonResponse ({'error':'Internal Fault, Try again later.'},status=500)

    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')




def employer_dashboard(request):
    return HttpResponse(request,"<h1>Welcome home</h1>");