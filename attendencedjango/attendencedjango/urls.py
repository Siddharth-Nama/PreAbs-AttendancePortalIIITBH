from django.contrib import admin
from django.urls import path, include, re_path
from login.views import *
from teacher.views import *
from students.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('home.urls')),  
    path('accounts/login/', loginStudent, name="loginStudent"),
    path('newRegistration/', newRegistration, name="newRegistration"),
    path('TeacherSection/', TeacherSection, name="TeacherSection"),
    path('StudentSection/', StudentSection, name="StudentSection"),
    re_path('^', include('django.contrib.auth.urls')),

]
