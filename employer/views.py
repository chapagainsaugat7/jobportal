from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Employer,Job,Questions
from django.contrib.auth.hashers import make_password,check_password
from django.core.files.storage import default_storage
from django.http import JsonResponse,HttpResponse
from jobseeker.models import AppliedJobs,JobSeeker,Score,ShortListedCandidates
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.urls import reverse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
import json,openpyxl
from datetime import datetime, time,timedelta
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
                location = data.get('location')
                try:
                    job = Job(
                              employer = employer,
                              job_type = type, 
                              job_position = position,
                              job_requirement = requirement,
                              job_description = description,
                              salary = salary,
                              location_type = location_type,
                              deadline = deadline,
                              location = location
                              )
                    job.save()
                    return JsonResponse({'Success':"Job added successfully."},status = 200)
                except Exception as e:
                    print(e)
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
                # print(jobs)
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
        allow_add = True #Initially employer can add questions.
        question_exists = Questions.objects.filter(job=job).exists()
        if question_exists:
            questions = Questions.objects.filter(job = job).order_by('question_id')
            paginator = Paginator(questions,3)
            page_number = request.GET.get('page')
            pages = paginator.get_page(page_number)
            total_pages = paginator.num_pages
            
        else:
            message = "Question doesn't exists."
            total_pages = 1
        
        today = datetime.today().date()
        if job.deadline < today:
            allow_add = False #if job deadline is expired. He cannot post questions.
        #Now displaying applicants for respected jobs.
        applicants = None
        applicant_not_found = ""
        try:
            applicants_exists = AppliedJobs.objects.filter(job = job).exists()
            if applicants_exists:
                applicants = AppliedJobs.objects.filter(job = job)
            else:
                applicant_not_found = "Applicants doesnt exists."
        except Exception as e:
            print(f"Exception querying applicants on view viewquestions - {e}")

        context = {
            'job':job,
            'view_question':view_question,
            'questions':questions,
            'message':message,
            'pages':pages,
            'lastpage':total_pages,
            'pagelist':[n+1 for n in range(total_pages)],
            'applicant_not_found':applicant_not_found,
            'applicants':applicants,
            'allowadd':allow_add
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
        messages.error(request,"Session Expired. Please login again.")
        return redirect('employer_signin')
    
def view_jobseeker(request,id):
    email = request.session.get('email',None)
    if email:
        jobseeker = JobSeeker.objects.get(id=id)
        context = {'data':jobseeker}
        return render(request,'employer-dashboard/components/viewjobseeker.html',context)
    else:
        messages.error(request,"Please login to visit this page.")
        return redirect('employer_signin')
    
def notices(request):
    email = request.session.get('email',None)
    if email:
        employer = Employer.objects.get(emp_email = email)
        jobs = Job.objects.filter(employer= employer)
        today = datetime.today().date()
        tommorow = today + timedelta(days=1)
        messages = []
        current_time = datetime.combine(datetime.today(),datetime.now().time())
        midnight = datetime.combine(datetime.today(),time())
        if jobs.exists():
            for job in jobs:
                applicants = AppliedJobs.objects.filter(job = job).count()
                if job.deadline == tommorow:
                    has_questions = Questions.objects.filter(job = job).exists()
                    view_url = reverse('viewjob',kwargs={'job_id':job.job_id})
                    message = f'Deadline for job you posted for position - {job.job_position} is tommorow.&nbsp;&nbsp;<a href="{view_url}">View</a>'
                    messages.append(message)

                    if not has_questions or applicants == 0:
                        question_url = reverse('viewquestions',kwargs={'id':job.job_id})
                        notice = f'<span>Job you posted for position {job.job_position} has no questions posted yet. It is scheduled to be deleted. &nbsp;&nbsp<a href={question_url}>View</a></span>'                                    
                        messages.append(notice)

                elif job.deadline == today and applicants > 0:
                    url = reverse('viewquestions',kwargs={'id':job.job_id})
                    message = f'<span>The deadline for your aaja job {job.job_position} is today. Please select the candidates from <a href="{url}">Here</a></span>'
                    messages.append(message)            
        else:
            message = 'No Questions are posted yet.'
            messages.append(message)
        context = {'job_message':messages}
        return render(request,"employer-dashboard/components/notices.html",context)
    else:
        messages.error(request,"Session Expired. Please login again.")
        return redirect('employer_signin')


def viewjob(request,job_id):
    email = request.session.get('email',None)
    if email:
        job = Job.objects.get(job_id=job_id)
        context = {'job':job}
        return render(request,"employer-dashboard/components/viewjobs.html",context)
    else:
        messages.error(request,"Session Expired. Please login again.")
        return redirect('employer_signin')

def updatejobs(request,id):
    email = request.session.get('email',None)
    if email:
        job = Job.objects.get(job_id = id)
        # print(job.salary)
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
        if request.method == 'POST':
            job_type = request.POST.get('job_type')
            position = request.POST.get('position')
            location = request.POST.get('location')
            position = request.POST.get('position')
            requirements = request.POST.get('requirements')
            description = request.POST.get('description')
            salary = request.POST.get('salary')
            deadline = request.POST.get('deadline')
            location_type = request.POST.get('location_type')
           
            if job_type == 'Job Type' or job_type == None or job_type == '':
                job_type = job.job_type

            if location_type == 'Location Type' or location_type == None or location_type == '':
                location_type = job.location_type

            if deadline == '' or deadline == None:
                deadline = job.deadline

            job.job_type = job_type
            job.job_position = position
            job.job_requirement = requirements
            job.location = location
            job.job_description = description
            job.salary = salary
            job.deadline = deadline
            try:
                job.save()
                messages.success(request,"Data updated sucessfully.")
                url = f'/employer/updatejobs/{job.job_id}'
                return redirect(url)

            except Exception as e:
                print(f'Exception updating jobs: {e}')
        context = {'job':job,'loc_type':LOCATION_TYPE,'job_type':JOB_TYPE}
        return render(request,'employer-dashboard/components/updatejobs.html',context)
    else:
        pass

def viewprogress(request,id,job_id):
    email = request.session.get('email',None)
    if email:
        jobseeker = JobSeeker.objects.get(id = id)
        job = Job.objects.get(job_id = job_id)
        score = Score.objects.get(jobseeker = jobseeker,job = job)
        applied_job = AppliedJobs.objects.get(job_seeker = jobseeker, job = job)
        shortlisted = False
        is_shortlisted = ShortListedCandidates.objects.filter(job = job, jobseeker = jobseeker).exists()
        if is_shortlisted:
            shortlisted = True
        context = {
            'jobseeker':jobseeker,
            'job':job,
            'score':score,
            'appliedjob':applied_job,
            'is_shortlisted':shortlisted
        }
        
        return render(request,'employer-dashboard/components/viewprogress.html',context)
    else:
        pass

def shortlistcandidate(request):
    email = request.session.get('email',None)
    id = None
    response = None
    if email:
        if request.method == 'POST':
            jobseeker_id = request.POST.get('candidate_id')
            job_id = request.POST.get('job_id')
            id = job_id
            jobseeker = JobSeeker.objects.get(id = jobseeker_id)
            job = Job.objects.get(job_id = job_id)

            try:
                email = f'Dear {jobseeker.name}, We are pleased to inform you that you have been selected for an interview for the {job.job_position} by {job.employer.emp_name}. Congratulations!'
                jobseeker_email = jobseeker.email
                shortlist = ShortListedCandidates(job = job, jobseeker = jobseeker)
                jobseeker.is_shortlisted = True
                jobseeker.save()
                shortlist.save()
                status = send_mail('Interview Invitation',
                          email,
                          "email.rajankhanal@gmail.com",
                          [jobseeker_email],
                          fail_silently=False)
                if status == 1:
                    print("Email sent")
                else:
                    print("Email not send.")

            except Exception as e:
                print(f'Exception in shortlistcandidate view - {e}')
        return redirect('employer_dashboard')

    else:
        return redirect('employer_signin')

def viewfinalcandidates(request,id):
    email = request.session.get('email',None)
    if email:
        job = Job.objects.get(job_id = id)
        candidate_exists = ShortListedCandidates.objects.filter(job = job).exists()
        context = {"has_candidates":candidate_exists,'job':job}
        if candidate_exists:
            candidates = ShortListedCandidates.objects.filter(job = job)
            context["candidates"] = candidates
        else:
            pass
            
        # print(context)
        return render(request,'employer-dashboard/components/shortlists.html',context)
    else:
        return redirect('employer_signin')
    
def downloadpdf(request,job_id):
    email = request.session.get('email',None)
    if email:
        try:
            job = Job.objects.get(job_id = job_id)
            candidates = ShortListedCandidates.objects.filter(job = job)
            context = {'candidates':candidates,'job':job}
            template = get_template('employer-dashboard/components/downloadpdf.html')
            html = template.render(context)
            pdf_buffer = BytesIO()
            pisa.CreatePDF(html, dest=pdf_buffer)
            pdf_buffer.seek(0)
            response = HttpResponse(pdf_buffer,content_type='application/pdf')
            response['Content-Disposition'] = f'filename="shortlistfor{job.job_position}.pdf"'
            return response
        except Exception as e:
            print(f'Error generating pdf on downloadpdf - {e}')
    else:
        return redirect('employer_signin')
def downloadxlsx(request,job_id):
    email = request.session.get('email', None)
    if email:
        try:
            job = Job.objects.get(job_id = job_id)
            candidates = ShortListedCandidates.objects.filter(job = job)
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.title = f'Shortlist for {job.job_position}'
            # Setting column headers.
            worksheet['A1'] = "S.N."
            worksheet['B1'] = "Name"
            worksheet['C1'] = "Address"
            worksheet['D1'] = "Email Address"
            worksheet['E1'] = "Phone Number"
            # Starts from column 2.
            row_num = 2
            sn = 1
            for candidate in candidates:
                worksheet[f'A{row_num}'] = sn
                worksheet[f'B{row_num}'] = candidate.jobseeker.name
                worksheet[f'C{row_num}'] = candidate.jobseeker.address
                worksheet[f'D{row_num}'] = candidate.jobseeker.email
                worksheet[f'E{row_num}'] = candidate.jobseeker.phone
                sn +=1 
                row_num +=1

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment;filename="shortlist_for_{job.job_position}.xlsx'
            workbook.save(response)
            return response
        except Exception as e:
            print(f"Exception in downloadxlsx view {e}")
    else:
        return redirect('employer_signin')
def logout_employer(request):
    logout(request)
    return redirect('employer_signin')