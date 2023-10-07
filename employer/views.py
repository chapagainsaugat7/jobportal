from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Employer,Job
from django.contrib.auth.hashers import make_password,check_password
from django.core.files.storage import default_storage
import json
from django.http import JsonResponse
from django.core import serializers
# logger = logging.getLogger(__name__)
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
        employer = Employer.objects.get(emp_email = email)
        if request.method == 'POST':
            if 'image' in request.FILES:
                if employer.emp_profile:
                    default_storage.delete(employer.emp_profile.path)
                
                image  = request.FILES['image']
                employer.emp_profile.save(image.name,image)

            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            about = request.POST.get('about')

            normalized_email = email.lower()
            employer.emp_name = name
            employer.emp_email = normalized_email
            employer.emp_phone_number = phone
            employer.about_employer = about
            
            try:
                employer.save()
                messages.info(request,"Profile successfully updated.")
            except Exception as e:
                print("Exception.....")
            

        data = employer
        return render(request,'employer-dashboard/components/employer-profile.html',{'data':data})
    else:
        messages.error(request,"Session Expired. Please Login again.")
        return redirect('employer_signin')
    

def post_jobs(request):
    email = request.session.get('email')
    if email:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            employer = Employer.objects.get(emp_email = email)
            if request.method == 'POST':
                data = json.load(request)
                type = data.get('type')
                position = data.get('job_position')
                requirement = data.get('job_requirement')
                description = data.get('job_description')
                salary = data.get('job_salary')
                deadline = data.get('job_deadline')
                location_type = data.get('location_type')
                try:
                    job = Job(
                              employer = employer,
                              job_type = type, 
                              job_position = position,
                              job_requirement = requirement,
                              job_description = description,
                              salary = salary,
                              location_type = location_type,
                              deadline = deadline
                              )
                    job.save()
                    return JsonResponse({'Success':"Job added successfully."},status = 200)
                except Exception as e:
                    # print(e)
                    return JsonResponse({'error':"Internal Server Error."}, status = 500)


        LOCATION_TYPE = (
                            ('Hybrid',"Hybrid"),
                            ('On Site',"On Site"),
                            ('Online',"Online")
                            )
        JOB_TYPE = (
                ('Full time',"Full Time"),
                ('Part Time',"Part Time"),
                ('Freelance',"Freelance")
                )
        data = Employer.objects.get(emp_email = email)
        return render(request,'employer-dashboard/components/postjobs.html',{'data':data,'loc_type':LOCATION_TYPE,'job_type':JOB_TYPE})

def get_data(request):
    email = request.session.get('email')
    if email:

        try:
            employer = Employer.objects.get(emp_email = email)
            job_exists = Job.objects.filter(employer = employer).exists()
            if job_exists:
                jobs = Job.objects.filter(employer = employer)
                job_list = []
                for job in jobs:
                    job_data = {
                        'job_id': job.job_id,
                        'job_type': job.job_type,
                        'job_position': job.job_position,
                        'job_requirement': job.job_requirement,
                        'job_description': job.job_description,
                        'salary': job.salary,
                        'location_type': job.location_type,
                        'deadline': job.deadline.strftime('%Y-%m-%d %H:%M:%S'),  # Format the date as needed
                    }
                    job_list.append(job_data)
                    return JsonResponse({'data':job_list})
            else:
                return JsonResponse({'error':'Data not found'}, status = 400)
        except Exception as e:
            return JsonResponse({'error':"Data not found."})
        