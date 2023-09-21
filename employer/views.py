from django.shortcuts import render,redirect
from .models import Job
# Create your views here.

def register_employer(request):

    if request.method == 'POST':
        # name number email, type_of_hiring,password
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        type_of_hiring = request.POST.get('type_of_hiring')
        password = request.POST.get('password')

        message = ''
        if name or number or email or type_of_hiring or password == '':
            message = "Please fill all fields."
            redirect('employer_registration',send_message = message)
            
    
    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')
