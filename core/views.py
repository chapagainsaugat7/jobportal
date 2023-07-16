from django.shortcuts import render
# from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'index.html')

def register_job_seeker(request):
    return render(request,'forms/job_seeker.html')

def login(request):
    return render(request,'forms/login.html')


def register_employer(request):
    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')


def admin(request):
    return render(request,'admin-dashboard/adminlogin.html')

def admin_test(request):
    return render(request,'admin-dashboard/dashboard.html')