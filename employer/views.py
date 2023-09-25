from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Employer
# Create your views here.




def register_employer(request):

    if request.method == 'POST':
        # name number email, type_of_hiring,password
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # normaline email, 
        normalized_email = email.lower()

        if Employer.objects.filter(emp_email = normalized_email):
           return JsonResponse({'email_exists':"Email Exists. Please try again with new email address."})
           redirect('employer_registration')
        else:
            try:
                employer = Employer(emp_name = name,emp_phone_number = number,emp_email = email,emp_password = password)
                employer.save()
                return JsonResponse({'ok':'Account successfully created.'})
            except Exception as e:
                return JsonResponse ({'error':'An error occured.'})
                # print("Exception....")
            

    
    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')
