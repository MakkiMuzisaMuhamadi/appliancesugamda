from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
admin.site.site_title = 'Appliances Uganda'
admin.site.index_title = 'Welcome to Appliances Uganda Admin Panel'
admin.site.site_header = 'Appliances Uganda'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('mainApp.urls') ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)