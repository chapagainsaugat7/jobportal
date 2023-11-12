from django.db import models
from django.utils.html import format_html
import datetime,os,uuid
from .utility import default_deadline

def filepath(request,filename):
     old_filename = filename
     time_now = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
     filename  = "%s%s" % (time_now,old_filename)
     return os.path.join('employer-profile/',filename)

class Employer(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=50,null=False,blank=False,verbose_name='Employer name')
    emp_phone_number = models.CharField(max_length=11,null=False,blank=False,verbose_name='Employer number')
    emp_email = models.EmailField(verbose_name='Employer Email',null=False,blank=False,unique=True)
    emp_password = models.CharField(null=False,blank=False,verbose_name='Employer Password',max_length=255)
    about_employer = models.TextField(verbose_name='About Employer',blank=True,null=True)
    emp_profile = models.FileField(upload_to=filepath ,null=True,verbose_name='Profile Photo')
    date_joined = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.emp_name
    
    def image(self):
                return format_html('<img src="/media/{}" height=30 width=30 style="border-radius:50%">'.format(self.emp_profile.url))
    

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

class Job(models.Model):
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,related_name='job')
    job_id = models.AutoField(primary_key=True)
    job_type = models.CharField(max_length=50,choices=JOB_TYPE,blank=False,null=False ,verbose_name='Job type')
    job_position = models.CharField(verbose_name="Position",max_length=100,null=False,blank=False)
    job_requirement = models.CharField(verbose_name="Requirements",max_length=100,null=False,blank=False)
    job_description = models.TextField(verbose_name="Description",null=False,blank=False)
    salary = models.TextField(max_length=30,blank=True,null=True)
    location = models.TextField(max_length=40,blank=False, null= False, default="Kathmandu")
    location_type = models.TextField(choices=LOCATION_TYPE,blank=False)
    deadline = models.DateField(blank=False,null=False,default=default_deadline)

    def __str__(self):
        return f'{self.job_position} by {self.employer.emp_name}'
    

class Questions(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name = 'question')
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(verbose_name="Questions",max_length=150,blank=False,null=False)
    marks = models.CharField(max_length=50,null=False,blank=False,default=5)
    correct_answer = models.CharField(max_length=100,null=True)
    option_one = models.CharField(max_length=100,null=True)
    option_two = models.CharField(max_length=100,null=True)
    option_three = models.CharField(max_length=100, blank=True)
    option_four = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Questions'

    def __str__(self) -> str:
        return f'{self.question} - {self.job.employer.emp_name}'
