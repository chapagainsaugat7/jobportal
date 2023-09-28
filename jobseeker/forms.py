from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager

from . import models
from django import forms
from django.contrib.auth.hashers import make_password

User = get_user_model()


class JobSeekerForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=10, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    preferred_job_type = forms.CharField(

    )

    def save(self, commit):
        password = make_password(self.cleaned_data.get('password'))
        email = BaseUserManager.normalize_email(self.cleaned_data.get('email'))
        phone_number = self.cleaned_data.get('phone_number')
        preferred_job_type = self.cleaned_data.get('preferred_job_type')
        name = self.cleaned_data.get('name')

        job = models.JobSeeker(phone_number=phone_number, name=name, email=email, password=password,
                               preferred_job_type=preferred_job_type)
        if commit:
            job.save()
            return job

