from django.shortcuts import render

# Create your views here.

def register_employer(request):
    if request.method == 'POST':
        # name number email, type_of_hiring,password
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        type_of_hiring = request.POST.get('type_of_hiring')
        password = request.POST.get('password')

        

    return render(request,'forms/employer.html')


def employer_signin(request):
    return render(request,'forms/employer_login.html')
