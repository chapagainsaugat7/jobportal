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
                
                return redirect('employer_dashboard')

            except Exception as e:
                pass

    return render(request,'forms/employer.html')


def employer_signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        normalized_email = email.lower()
        try:
            employer = Employer.objects.get(emp_email__iexact = normalized_email)
            password_matched = check_password(password,employer.emp_password)
            if password_matched:
                request.session['email'] = normalized_email
                return redirect('employer_dashboard')
            else:
                messages.error(request,"Incorrect Password")
                return redirect('employer_signin')
        except Employer.DoesNotExist as e:
            print(e)
            messages.error(request,"Account doesnot exists.")
            return redirect('employer_signin')
    

    return render(request,'forms/employer_login.html')

# R@ju_1234


def employer_dashboard(request):
    email = request.session.get('email')
    if email:
        messages.info(request,"Plese complete building your company profile.")
        count = len([msg for msg in messages.get_messages(request) if msg.level == messages.INFO])
        data = Employer.objects.get(emp_email = email)
        return render(request,'employer-dashboard/index.html',{'data':data,'count':count})
    else:
        return redirect('employer_signin')
    



def company_profile(request):

    email = request.session.get('email')
    if email:
        if request.method == 'POST' and request.FILES:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            about = request.POST.get('about')
            image = request.FILES['image']

            normalized_email = email.lower()
            # Check if image is valid or not.
            valid_image = False
            if image:
                file_extension = image.name.split('.')[-1].lower()
                print("File extensioon is:",file_extension)
                allowed_extension = ['jpg','png','jpeg','svg']
                if file_extension not in allowed_extension:
                    print("File extension not supported.")
                    messages.error(request,"Not supported file extension.")
                else:
                   valid_image = True

            if valid_image:
                try:
                    pass

                except Exception as e:
                    pass

        data = Employer.objects.get(emp_email = email)
        return render(request,'employer-dashboard/components/employer-profile.html',{'data':data})
    else:
        messages.error(request,"Session Expired. Please Login again.")
        return redirect('employer_signin')