from django.contrib import admin
from jobseeker.models import JobSeeker,AppliedJobs,Score,ShortListedCandidates
# Register your models here.

admin.site.register(JobSeeker)
admin.site.register(AppliedJobs)
admin.site.register(Score)
admin.site.register(ShortListedCandidates)