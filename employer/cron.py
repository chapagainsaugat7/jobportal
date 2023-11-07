from .models import Job
from jobseeker.models import AppliedJobs
import datetime
def check_deadline():
    jobs = Job.objects.all()
    today = datetime.datetime.today().date()
    for job in jobs:
        if job.deadline == today:
            #now email employer saying that today is deadline. 
            pass
        elif job.deadline < today :
            #Job deadline is expires.
            #maybe delete the job if everything is done.
            pass
        else:
            #do nothing
            pass