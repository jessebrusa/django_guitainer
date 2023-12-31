from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
    path('', include('login.urls')),
    path('', include('obtain.urls')),
    path('', include('groups.urls')),   
    path('', include('dashboard.urls')),   
]
