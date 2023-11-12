from django.urls import path
from .views import *

urlpatterns = [
    path('register_employer/',register_employer,name='employer_registration'),
    path('login_employer/',employer_signin,name="employer_signin"),
    path('employer_dashboard/',employer_dashboard,name="employer_dashboard"),
    path('company_profile/',company_profile,name="company_profile"),
    path("postjobs/", post_jobs, name="postjobs"),
    path('getdata/',get_data,name="getjobs"),
    path('questions/',questions,name="questions"),
    path('applicants/',applicants,name='applicants'),
    path('viewquestions/<int:id>',viewquestions,name="viewquestions"),
    path('view_jobseeker/<uuid:id>',view_jobseeker,name='view_jobseeker'),
    path('viewjob/<int:job_id>',viewjob,name="viewjob"),
    path('logout_employer/',logout_employer,name='logout_employer'),
    path('notices/',notices,name="notices"),
    path('shortlistcandidate/',shortlistcandidate,name="shortlistcandidate"),
    path('updatejobs/<int:id>',updatejobs,name='updatejob'),
    path('viewprogress/<uuid:id>/<int:job_id>',viewprogress,name="viewprogress"),
    path('viewfinalcandidates/<int:id>',viewfinalcandidates,name="viewfinalcandidates"),
    path('downloadpdf/<int:job_id>',downloadpdf,name='downloadpdf'),
    path('downloadxlsx/<int:job_id>',downloadxlsx,name='downloadxlsx'),
]