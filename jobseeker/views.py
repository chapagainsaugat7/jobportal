from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from jobseeker.models import JobSeeker

def register_job_seeker(request):
    if request.method == 'POST':
        name = request.POST.get('jname')
        phone_number = request.POST.get('jphone')
        email = request.POST.get('jemail')
        password = request.POST.get('jpassword')

        normalized_email = email.lower()

        hashed_password  = make_password(password)
        message = ''
        email_exists = JobSeeker.objects.filter(email = normalized_email).exists()
        phone_exists = JobSeeker.objects.filter(phone = phone_number).exists()

        if email_exists:
            message = 'Email Already Exists'
        elif phone_exists:
            message = 'Phone Number is Taken'

        if email_exists or phone_exists:
            messages.error(request,message)
            return render(request,'forms/job_seeker.html')
        
        else:
            jobseeker = JobSeeker(name=name,phone=phone_number,email=normalized_email,password=hashed_password)
            try:
                jobseeker.save()
                request.session['email'] = normalized_email
                return redirect('jobseeker-dashboard')
            except Exception as e:
                messages.add(request,"Internal Server Error. Please try again later.")
                return redirect('register_jobseeker')
    return render(request,'forms/job_seeker.html')

def login(request):
    return render(request,'forms/login.html')

def jobseeker_dashboard(request):
    return render(request,'jobseeker-dashboard/dashboard.html')

def create_profile(request):
    nav_items = ["Home","Qualification","Preferences"]
    return render(request,"jobseeker-dashboard/components/createprofile.html",{"nav_items":nav_items})


def profile(request):
    return render(request,'jobseeker-dashboard/components/profile.html')