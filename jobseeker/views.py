from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.contrib.auth import logout
from jobseeker.models import JobSeeker
from employer.models import Job,Employer
from django.views.decorators.clickjacking import xframe_options_exempt

import uuid
from django.core.files.storage import default_storage
def register_job_seeker(request):
    if request.method == 'POST':
        name = request.POST.get('jname')
        phone_number = request.POST.get('jphone')
        email = request.POST.get('jemail')
        password = request.POST.get('jpassword')
        normalized_email = email.lower()
        hashed_password  = make_password(password)

        email_exists = JobSeeker.objects.filter(email = normalized_email).exists()
        phone_exists = JobSeeker.objects.filter(phone = phone_number).exists()

        message = ''
        if email_exists:
            message = 'Email Already Exists'
        elif phone_exists:
            message = 'Phone Number is Taken'

        if email_exists or phone_exists:
            messages.error(request,message)
            return render(request,'forms/job_seeker.html')
        
        else:
            #name email password phone
            pk = uuid.uuid4()
            jobseeker = JobSeeker(id = pk,name=name,email=normalized_email,password=hashed_password,phone = phone_number)
            try:
                jobseeker.save()
                request.session['email'] = normalized_email
                return redirect('jobseeker-dashboard')
            except Exception as e:
                print(e)
                messages.error(request,"Internal Server Error. Please try again later.")
                return redirect('register_jobseeker')
            
    return render(request,'forms/job_seeker.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        normalized_email = email.lower()

        # print(normalized_email,password)

        message = ''
        if email == '':
            message = "Email address is required."
        
        elif password =='':
            message = "Password is required."

        if email =='' or password == '':
            messages.error(request,message)
            return redirect('login')

        else:
            jobseeker_exists = JobSeeker.objects.filter(email = normalized_email).exists()
            if jobseeker_exists:
                jobseeker = JobSeeker.objects.get(email = normalized_email)
                password_matched = check_password(password,jobseeker.password)
                if password_matched:
                    request.session['jobseeker_email'] = normalized_email
                    return redirect('jobseeker-dashboard')
                else:
                    messages.error(request,"Password doesn't matched.")
                    return redirect('login')
            else:
                messages.error(request,"Account with provided email doesn't exists.")
                return redirect('register_jobseeker')
    return render(request,'forms/login.html')


def jobseeker_dashboard(request):
    email = request.session.get('jobseeker_email',None)
    if email:
        job = Job.objects.all()
        # print(job)
        return render(request,'jobseeker-dashboard/dashboard.html',{'job':job})
    else:
        messages.error(request,"Session Expired. Please login here.")
        return redirect('login')

def create_profile(request):
    nav_items = ["Home","Qualification","Preferences"]
    return render(request,"jobseeker-dashboard/components/createprofile.html",{"nav_items":nav_items})

@xframe_options_exempt
def profile(request):
    email_add = request.session.get('jobseeker_email',None)
    if email_add:
        if request.method == 'POST':
            name = request.POST.get('name')
            # email = request.POST.get('email') Should not be changed randomly.
            address = request.POST.get('address')
            phone =  request.POST.get('phone')
            dob = request.POST.get('dob','')
            preference = request.POST.get('preference')
            qualification = request.POST.get('qualification')
            aboutyou = request.POST.get('aboutyou')
            cv = request.FILES.get('cv',None)
            # print(preference)
            # normalized_email = email.lower()
            if dob == '':
                pass
            else:
                jobseeker.date_of_birth = dob

            jobseeker = JobSeeker.objects.get(email = email_add)
            if 'profile' in request.FILES:
                if jobseeker.profile:
                    default_storage.delete(jobseeker.profile.path)
                
                image  = request.FILES['profile']
                jobseeker.profile.save(image.name,image)
            
            if 'cv' in request.FILES:
                if jobseeker.cv:
                    default_storage.delete(jobseeker.cv.path)
                
                cv = request.FILES.get('cv')
                jobseeker.cv.save(cv.name,cv)
            


            jobseeker.name = name
            jobseeker.address = address
            jobseeker.phone = phone
            jobseeker.preferences = preference
            jobseeker.about_me = aboutyou
            jobseeker.qualification = qualification
            
            try:
                jobseeker.save()
            except Exception as e:
                print(e)

        jobseeker = JobSeeker.objects.get(email = email_add)
        # print("CV...",jobseeker.cv.url)

        return render(request,'jobseeker-dashboard/components/profile.html',{'data':jobseeker})
    else:
        messages.error(request,"Session Expired. Please login here.")
        return redirect('login')
    

def logout_jobseeker(request):
    logout(request)
    return redirect('home_page')


def browse_job(request,id):
    email = request.session.get('jobseeker_email',None)
    if email:
        try:
            job = Job.objects.get(job_id = id)
        except:
            pass
        return render(request,'jobseeker-dashboard/components/browsejobs.html',{"data":job})

    else:
        messages.error(request,"Session Expired. Please Login again.")
        return redirect('login')
    
def view_employer(request,employer):
    email = request.session.get('jobseeker_email',None)
    if email:
        try:
            employer = Employer.objects.get(emp_id = employer)
            # print(employer.emp_phone_number)
            # print(employer.emp_profile)
        except Exception as e:
            pass
        return render(request,'jobseeker-dashboard/components/aboutemployer.html',{'employer':employer})
    else:
        messages.error(request,"Session Expired. Please Login again.")
        return redirect('login')

