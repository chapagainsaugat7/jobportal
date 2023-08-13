from django.db import models

# Employer posts job has JobQuestions.
class Employer(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=50,null=False,blank=False,verbose_name='emp_name')
    emp_phone_number = models.CharField(max_length=11,null=False,blank=False,verbose_name='emp_number')
    emp_job_type = models.CharField(max_length=50,default="Full Time",blank=False,null=False)
    emp_email = models.EmailField(verbose_name='emp_email',null=False,blank=False,unique=True)
    emp_password = models.CharField(max_length=25,null=False,blank=False,verbose_name='emp_password')
    about_employer = models.TextField(verbose_name='emp_about',blank=True,null=True)
    emp_profile = models.FileField(upload_to='employer-profile/',null=True)

    def __str__(self):
        return self.name
    

LOCATION_TYPE = (
    ('Hybrid',"Hybrid"),
    ('On Site',"On Site"),
    ('Online',"Online")
    )

class Job(models.Model):
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE)
    job_id = models.AutoField(primary_key=True)
    job_position = models.CharField(verbose_name="Position",max_length=100,null=False,blank=False)
    job_requirement = models.CharField(verbose_name="Requirements",max_length=100,null=False,blank=False)
    job_description = models.TextField(verbose_name="Description",null=False,blank=False)
    salary = models.TextField(max_length=30,blank=True,null=True);
    location_type = models.TextField(choices=LOCATION_TYPE,blank=False)

class Questions(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name = 'question')
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(verbose_name="Questions",max_length=150,blank=False,null=False)
    marks = models.CharField(max_length=50,null=False,blank=False,default=5)


class Answers(models.Model):
    question = models.ForeignKey(Questions, related_name='question_answer',on_delete=models.CASCADE)
    answer = models.CharField(max_length=100,null=False,blank=False)
    is_answer_correct = models.BooleanField(default=False)

