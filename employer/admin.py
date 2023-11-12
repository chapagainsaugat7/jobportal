from django.contrib import admin
from .models import *
# Register your models here.
class EmployerAdmin(admin.ModelAdmin):
    list_display = ("emp_name", "emp_phone_number", "emp_email",)
    search_fields  = ("emp_name",)

class JobAdmin(admin.ModelAdmin):
    list_display=('employer','job_type','job_position','job_requirement','location','salary','deadline',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('job','question','marks','correct_answer',)

admin.site.register(Employer,EmployerAdmin)
admin.site.register(Job,JobAdmin)
admin.site.register(Questions,QuestionAdmin)
