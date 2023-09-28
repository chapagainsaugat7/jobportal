from django.db import models

PREFERRED_JOB_CATEGORY = (
    (0, 'IT'),
    (1, 'Education'),
)


class JobSeeker(models.Model):
    phone = models.CharField(max_length=10)  # India must be validated with regex or something
    job_category = models.PositiveSmallIntegerField(choices=PREFERRED_JOB_CATEGORY,
                                                    default=PREFERRED_JOB_CATEGORY[0][0])
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=50)


class AppliedJobs(models.Model):
    pass
