from django.db import models
from employer.models import Job
import datetime
import os,uuid

def filepath(request,filename):
    old_filename = filename
    time_now = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename  = "%s%s" % (time_now,old_filename)
    return os.path.join('jobseeker-cv/',filename)

def profilepath(request,filename):
    old_filename = filename
    time_now = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (time_now,old_filename)
    return os.path.join('jobseeker-profile/',filename)


class JobSeeker(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50,null=False,blank=False,verbose_name='Jobseeker Name')
    email = models.EmailField(null=False, blank=False, unique=True,verbose_name='Jobseeker Email')
    password = models.TextField(max_length=255,blank=False,null=False,verbose_name='Jobseeker Password')
    phone = models.TextField(max_length=15,blank=False,null=False,verbose_name='Jobseeker Phone')
    address = models.TextField(max_length=50,blank=True,null=True,default="Kathmandu",verbose_name='Address')
    date_of_birth = models.DateField(null=True, blank=True)
    about_me = models.TextField(null=True,blank=True,verbose_name='About You')
    qualification = models.TextField(blank=True,null=True,verbose_name="Qualifications")
    experiences = models.TextField(blank = True,null=True,verbose_name='Experiences')
    preferences = models.TextField(null=True,blank=True,verbose_name="Job Preferences")
    cv = models.FileField(upload_to=filepath,verbose_name='CV')
    profile = models.FileField(upload_to=profilepath,verbose_name='Profile')

    def __str__(self):
        return self.name
    
class AppliedJobs(models.Model):
    id = models.UUIDField(primary_key=True)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker,on_delete=models.CASCADE)
    coverletter = models.TextField(null=False,blank=False,verbose_name="Cover Letter",default='')

    class Meta:
        verbose_name_plural = 'Applied Jobs'
    def __str__(self) -> str:
        return f'Applied For: {self.job.job_position} by {self.job_seeker.name}'
    

class Score(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    jobseeker = models.ForeignKey(JobSeeker,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    score = models.IntegerField(null=True,blank=True)

    def __str__(self) -> str:
        return f'Score of {self.jobseeker.name}'
