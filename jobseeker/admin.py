from django.contrib import admin
from jobseeker.models import JobSeeker,AppliedJobs
# Register your models here.

admin.site.register(JobSeeker)
admin.site.register(AppliedJobs)