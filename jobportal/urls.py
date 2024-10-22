from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from jobportal.views import home
admin.site.site_header = "Job Portal Administration"
admin.site.site_title ="Admin area"
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('',home,name="home_page"),
    path('jobseeker/',include('jobseeker.urls')),
    path('employer/',include('employer.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
