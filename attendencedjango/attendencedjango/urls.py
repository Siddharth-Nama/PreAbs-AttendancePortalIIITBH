from django.contrib import admin
from django.urls import path, include, re_path
from login.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('home.urls')),  
    path('accounts/login/', loginStudent, name="loginStudent"),
    path('newRegistration/', newRegistration, name="newRegistration"),
    re_path('^', include('django.contrib.auth.urls')),
]
