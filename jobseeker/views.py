import json

from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render
from django.http import JsonResponse
from . import models, forms

User = get_user_model()


def register_job_seeker(request):
    if request.method == 'POST':
        form = forms.JobSeekerForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            return JsonResponse({"message": job}, status=200)
    form = forms.JobSeekerForm()

    return render(request, 'forms/job_seeker.html', {"form": form})


def login(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == "POST":
            data = json.load(request)
            email = data.get('email')
            password = data.get('password')
            remember_me = data.get('remember_me')

            if remember_me == "true":
                pass
            else:
                request.session.set_expiry(0)

            user = User.objects.get(email=email)
            account = authenticate(username=user.username, password=password)
            if account is not None:
                if user.is_active:
                    # login(request, usr) django login auth function for session
                    # Generate JWT Token here
                    return JsonResponse(status=200, data=None)
            else:
                data = json.dumps({
                    'message': 'cannot login with given credentials'
                })
                return JsonResponse(status=403, data=data)

    return render(request, 'forms/login.html')


def jobseeker_dashboard(request):
    return render(request, 'jobseeker-dashboard/dashboard.html')


def create_profile(request):
    nav_items = ["Home", "Qualification", "Preferences"]
    return render(request, "jobseeker-dashboard/components/createprofile.html", {"nav_items": nav_items})


def profile(request):
    return render(request, 'jobseeker-dashboard/components/profile.html')
