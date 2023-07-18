from django.shortcuts import render

# Create your views here.

def register_employer(request):
    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')
