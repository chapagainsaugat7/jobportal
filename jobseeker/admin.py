from django.contrib import admin
from jobseeker.models import JobSeeker,AppliedJobs,Score
# Register your models here.

admin.site.register(JobSeeker)
admin.site.register(AppliedJobs)
admin.site.register(Score)