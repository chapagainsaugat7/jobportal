from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.contrib.auth import logout
from jobseeker.models import JobSeeker,AppliedJobs,Score,ShortListedCandidates
from employer.models import Job,Employer,Questions
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.db.models import Q
from django.urls import reverse
import uuid
import json
import datetime,time
import random
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
        job = Job.objects.order_by('job_id')
        paginator = Paginator(job,6)
        page_number = request.GET.get('page')
        pages = paginator.get_page(page_number)
        total_pages = paginator.num_pages #Returns total number of pages.
        jobseeker = JobSeeker.objects.get(email = email)
        context={'job':job,
                 'pages':pages,
                 'lastpage':total_pages,
                 'pagelist':[n+1 for n in range(total_pages)],
                 'profile':jobseeker.profile.url
                 }
        return render(request,'jobseeker-dashboard/dashboard.html',context)
    else:
        messages.error(request,"Session Expired. Please login here.")
        return redirect('login')

def statistics(request):
    email = request.session.get('jobseeker_email',None)
    if email:
        jobseeker = JobSeeker.objects.get(email = email)
        message = ''
        applied_jobs = None
        has_applied = AppliedJobs.objects.filter(job_seeker = jobseeker).exists()
        if has_applied:
            applied_jobs = AppliedJobs.objects.filter(job_seeker = jobseeker)

        else:
            message = 'You havenot applied to any jobs yet.'
        
        jobs = Job.objects.all()
        recommend_jobs = set()
        for job in jobs:
           matching_jobs = Job.objects.filter(location = jobseeker.address)
        #    print(matching_jobs)
           if matching_jobs.exists():
               recommend_jobs.update(matching_jobs)

        recommend_jobs = list(recommend_jobs)
        
        context = {
            'message':message,
            'applied_jobs':applied_jobs,
            'recommend_jobs':recommend_jobs,
            'profile':jobseeker.profile.url
        }
        return render(request,'jobseeker-dashboard/components/statistics.html',context)
    else:
        messages.error(request,"Session Expired. Please Login here.")
        return redirect('login')
    
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
            experiences = request.POST.get('experiences')
            jobseeker = JobSeeker.objects.get(email = email_add)
            if dob == '':
                pass
            else:
                jobseeker.date_of_birth = dob

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
            jobseeker.experiences = experiences           
            try:
                jobseeker.save()
            except Exception as e:
                print(e)

        jobseeker = JobSeeker.objects.get(email = email_add)
        return render(request,'jobseeker-dashboard/components/profile.html',{'data':jobseeker,'profile':jobseeker.profile.url})
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
            allow = True
            job = Job.objects.get(job_id = id)
            jobseeker = JobSeeker.objects.get(email=email)
            is_applied = AppliedJobs.objects.filter(job__job_id = id,job_seeker__id = jobseeker.id).exists()
            message = ''
            has_score = Score.objects.filter(jobseeker = jobseeker, job = job).exists()
            allow_for_quiz = True
            # Prevent jobseeker from applying job after deadline
            if datetime.date.today() > job.deadline:
                allow = False
                message = "Application closed."                
            

            if is_applied:
                allow = False
                allow_for_quiz = True
                message = "You've already applied for this job."
            
            else:
                allow_for_quiz = False

            if has_score:
                allow_for_quiz = False
                message = "You've given a test. We will inform you soon about your progess."
            else:
                message = ""
            

            # print(is_applied)
        except Exception as e:
            print(f"Exception in browse_job:{e}")
        context = {"data":job,"allowed":allow,"message":message,"isapplied":is_applied,"allowed_for_quiz":allow_for_quiz,'profile':jobseeker.profile.url}
        return render(request,'jobseeker-dashboard/components/browsejobs.html',context)

    else:
        messages.error(request,"Session Expired. Please Login again.")
        return redirect('login')
    
def view_employer(request,employer):
    email = request.session.get('jobseeker_email',None)
    if email:
        try:
            jobseeker = JobSeeker.objects.get(email = email)
            employer = Employer.objects.get(emp_id = employer)
        except Exception as e:
            pass
        return render(request,'jobseeker-dashboard/components/aboutemployer.html',{'employer':employer,'profile':jobseeker.profile.url})
    else:
        messages.error(request,"Session Expired. Please Login again.")
        return redirect('login')

def download_cv(request,jobseeker_id):
    email = request.session.get('jobseeker_email',None)
    if email:
        try:
            # print("Entering try")
            jobseeker = JobSeeker.objects.get(id = jobseeker_id)

            context = {'data':jobseeker}
            template = get_template('jobseeker-dashboard/components/downloadcv.html')
            html = template.render(context)
            pdf_buffer = BytesIO()
            pisa.CreatePDF(html, dest=pdf_buffer)
            pdf_buffer.seek(0) #set buffer position to start.
            response = HttpResponse(pdf_buffer,content_type='application/pdf')
            response['Content-Disposition'] = f'filename="{jobseeker.name}_CV.pdf"'
            return response
        except Exception as e:
            pass
    else:
        messages.error(request,"Please Sign in here.")
        return redirect('login')

def applyjob(request):
    email = request.session.get('jobseeker_email',None)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if email:
        if is_ajax:
            if request.method == 'POST':
                data = json.load(request)
                coverletter = data.get('coverletter')
                job_id = data.get('job_id')
                job = Job.objects.get(job_id = job_id)
                jobseeker = JobSeeker.objects.get(email = email)
                try:
                    pk = uuid.uuid4()
                    appliedjobs = AppliedJobs(id = pk, job = job,job_seeker = jobseeker,coverletter = coverletter)
                    appliedjobs.save()
                    response_data = {'success': 'Application received.'}
                    return HttpResponse(json.dumps(response_data),content_type = 'application/json',status=200)
                except Exception as e:
                    print("Exception in applyjob view",e)
    
    else:
        messages.error(request,"Please Sign in before you proceed")
        return redirect('login')

def quiz(request,id):
   email = request.session.get('jobseeker_email',None)
   if email:
       jobseeker = JobSeeker.objects.get(email = email)
       #check if this jobseeker has applied a job or not.
       has_applied = AppliedJobs.objects.filter(job_seeker = jobseeker,job_id = id).exists()
       if has_applied:
           job = Job.objects.get(job_id = id)
           has_quiz = Questions.objects.filter(job = job).exists()
           if has_quiz:
               quizes = Questions.objects.filter(job= job).order_by('question_id')
               paginator = Paginator(quizes,1)
               page_number = request.GET.get('page')
               page_obj = Paginator.get_page(paginator,page_number)
               context = {'jobseeker':jobseeker,'pages':page_obj}
               if request.method == 'GET':
                   if page_number == None:
                       request.session['total_score'] = 0
                   next_page = request.path_info+"?page="+request.GET.get("page",'1') 
                   request.session['next_page'] = next_page
                   return render(request,'jobseeker-dashboard/quiz.html',context)
               
               is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
               if request.method == 'POST':
                   if is_ajax:
                       data = json.load(request)
                       user_answer = data.get('userAnswer')
                       question_id = data.get('questionId')
                       #select correct answer from questions where id = question_id
                       db_query = Questions.objects.get(question_id = question_id)

                       if db_query.correct_answer == user_answer:
                           total_score = request.session.get('total_score',0)
                           total_score += 5
                           request.session['total_score'] = total_score
                           print(request.session.get('total_score',0))
                           return HttpResponseRedirect(request.session.get('next_page'))
                       else:
                           return HttpResponseRedirect(request.session.get('next_page'))
               if request.method == 'POST':
                   user_score = request.session.get('total_score')
                   print(user_score)
                   try:
                       score = Score(jobseeker = jobseeker,job = job,score = user_score)
                       score.save()
                       print("Data saved.")
                       return JsonResponse({'status':"Score saved successfully.",'message':"We will email you soon."})
                   except Exception as e:
                       print(e)
                       return JsonResponse({'error':'Trouble saving score.'})                             
           else:
               return render(request,'jobseeker-dashboard/browsejobs.html',{"message":"No quiz exists."})
               
       else:
           message = "You haven't applied for this job."
           return render(request,'jobseeker-dashboard/components/browsejobs.html',{"message":message})
           
   else:
       messages.error(request,"Please sign in here.")
       return redirect('login')
   
def search_job(request):
    email = request.session.get('jobseeker_email',None)
    if email:
        if request.method == 'GET':
            # print(request.method)
            search_query = request.GET.get('jobName')
            # print(f'SEarch Query {search_query}')
            jobseeker = JobSeeker.objects.get(email = email)
            if search_query == '' or search_query == None:
                return redirect('jobseeker-dashboard')
            else:
                try:
                    # Here Django ORM does not stores data in sorted order.
                    # So, we cannot implement binary search algorithm.
                    # Now we can do is linear search.

                    all_jobs = Job.objects.all()
                    #Performing linear search with partial matching (Case insensitive.)
                    matching_jobs = [job for job in all_jobs if search_query.lower() in job.job_position.lower()]
                    # Pagination
                    paginator = Paginator(matching_jobs,6)
                    page_number = request.GET.get('page')
                    page_obj = Paginator.get_page(paginator,page_number)
                    total_pages = paginator.num_pages
                    if matching_jobs:
                        context  = {'pages':page_obj,
                                    'page_list':[n+1 for n in range(total_pages)],
                                    'job_exists':True,
                                    'lastpage':total_pages,
                                    'profile':jobseeker.profile.url}
                        return render(request,'jobseeker-dashboard/components/searchresult.html',context)
                    else:
                        context = {'message':"No matching job found.",'profile':jobseeker.profile.url}
                        return render(request,"jobseeker-dashboard/components/searchresult.html",context)
                except Exception as e:
                    print(f'Exception searching job {e}')
                    return redirect('jobseeker-dashboard')

        return render(request,'jobseeker-dashboard/components/searchresult.html')
    else:
       messages.error(request,"Please sign in here.")
       return redirect('login')

