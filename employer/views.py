from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Employer,Job,Questions
from django.contrib.auth.hashers import make_password,check_password
from django.core.files.storage import default_storage
from django.http import JsonResponse
from jobseeker.models import AppliedJobs
from django.core.paginator import Paginator
import json

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
    email = request.session.get('email',None)
    if email:
        messages.info(request,"Plese complete building your company profile.")
        count =len([msg for msg in messages.get_messages(request) if msg.level == messages.INFO])
        try:
            employer = Employer.objects.filter(emp_email = email).first()
            if employer:
               data = Employer.objects.get(emp_email = email)
        except Exception as e:
            pass
        return render(request,'employer-dashboard/index.html',{'data':data,'count':count})
    else:
        messages.error(request,"Session Expired. Please sign in again.")
        return redirect('employer_signin')
    



def company_profile(request):

    email = request.session.get('email',None)
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
    email = request.session.get('email',None)
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
    email = request.session.get('email',None)
    if email:

        try:
            employer = Employer.objects.get(emp_email = email)
            job_exists = Job.objects.filter(employer = employer).exists()
            if job_exists:
                jobs = employer.job.all()
                print(jobs)
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
                # print("data",job_list)
                return JsonResponse({'data':job_list})
            else:
                return JsonResponse({'error':'Data not found'}, status = 400)
        except Exception as e:
            print(e)
            return JsonResponse({'error':"Data not found."})
        

def questions(request):
    email = request.session.get('email',None)
    if email:
        #Display job, question answer, schedule
        employer = Employer.objects.get(emp_email = email)       
        job_exists = Job.objects.filter(employer = employer).exists()
        jobs = None
        message = ''
        if job_exists:
            jobs = Job.objects.filter(employer = employer).order_by('job_id')
        else:
            message = 'No jobs posted yet.'
            

        context = {
            'jobs':jobs,
            'message':message
        }

        return render(request,'employer-dashboard/components/questions.html',context)
    else:
        messages.error(request,"Session Expired.")
        return redirect('employer_signin')

def viewquestions(request,id):
    email = request.session.get('email',None)
    if email:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':
                 data = json.load(request)
                 job_id = data.get('job_id')
                 question = data.get('question')
                 correct_answer = data.get('correctAnswer')
                 opt1 = data.get('opt1')
                 opt2 = data.get('opt2')
                 opt3 = data.get('opt3')
                 opt4 = data.get('opt4')

                 try:
                     job = Job.objects.get(job_id = job_id)
                     #job question correct_answer 4 ota option_one
                     question = Questions(job = job,question = question,correct_answer=correct_answer,option_one=opt1,option_two=opt2,option_three=opt3,option_four=opt4)
                     
                     question.save()
                 except Exception as e:
                    print(f'Exception in viewquestions view - {e}')



        employer = Employer.objects.get(emp_email = email)
        job = Job.objects.get(employer = employer,job_id = id)

        message = ''
        questions = None
        paginator = None
        page_number = None
        total_pages = None
        pages = None
        view_question =None
        question_exists = Questions.objects.filter(job=job).exists()
        if question_exists:
            questions = Questions.objects.filter(job = job).order_by('question_id')
            paginator = Paginator(questions,3)
            page_number = request.GET.get('page')
            pages = paginator.get_page(page_number)
            total_pages = paginator.num_pages
        
        else:
            message = "Question doesn't exists."
        
        view_id = request.GET.get('view')
        try:
            view_question = Questions.objects.get(question_id = view_id)
            

        except Exception as e:
            pass

        context = {
            'job':job,
            'view_question':view_question,
            'questions':questions,
            'message':message,
            'pages':pages,
            'lastpage':total_pages,
            'pagelist':[n+1 for n in range(total_pages)]
        }
        return render(request,'employer-dashboard/components/viewquestions.html',context)
    else:
        messages.error(request,"Session Expired.")
        return redirect('employer_signin')



def applicants(request):
    email = request.session.get('email',None)
    if email:
        #check employer information
        applicants = {}
        message = ''

        employer = Employer.objects.get(emp_email = email)
        #one employer can post multiple jobs.
        jobs = Job.objects.filter(employer = employer)
        
        #now check if jobs have applicants. 
        for job in jobs:
            applicant = AppliedJobs.objects.filter(job = job)
            if applicant.exists():
                applicants[job] = applicant
        
        return render(request,'employer-dashboard/components/applicants.html',{'message':message,'data':applicants})
    else:
        messages.error("Session Expired. Please login again.")
        return redirect('employer_signin')