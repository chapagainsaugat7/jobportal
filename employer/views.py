from django.shortcuts import render,redirect
from django.contrib import messages
from urllib.parse import urlencode
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
        normalized_email = email.lower()
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
            #emp_name, emp_phone_number emp_email emp_password
            employer = Employer(emp_name = name,emp_phone_number = number,emp_email = normalized_email,emp_password = hashed_password)
            try:
                '''
                    save data into database
                    set session variable and redirect to dashboard.
                '''
                employer.save()
                request.session['email'] = normalized_email
                # set session data, encode url and redirect to dashboard.
                data = {'email': request.session.get('email')}
                params = urlencode(data)
                redirect_url = f'employer_dasboard/?{params}'
                print(redirect_url)
                return redirect(redirect_url)

            except Exception as e:
                pass

    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')

# R@ju_1234


def employer_dashboard(request):
    email = request.session.get('email')
    if email:
        data = Employer.objects.get(emp_email = email)
        return render(request,'employer-dashboard/index.html',{'data':data})
    else:
        return redirect('employer_signin')
    