from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('',include('core.urls')),
    path('jobseeker/',include('jobseeker.urls')),
    path('employer/',include('employer.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
