from django.shortcuts import render

# Create your views here.


def register_job_seeker(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        

    return render(request,'forms/job_seeker.html')

def login(request):
    return render(request,'forms/login.html')

def jobseeker_dashboard(request):
    return render(request,'jobseeker-dashboard/dashboard.html')

def create_profile(request):
    nav_items = ["Home","Qualification","Preferences"]
    return render(request,"jobseeker-dashboard/components/createprofile.html",{"nav_items":nav_items})


def profile(request):
    return render(request,'jobseeker-dashboard/components/profile.html')