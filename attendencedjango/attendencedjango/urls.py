from django.contrib import admin
from django.urls import path, include
from login.views import loginStudent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('home.urls')),  
    path('login/', loginStudent, name="login"), 
    path('Student/', Student, name="Student"), 
    path('Teacher/', Teacher, name="Teacher"), 
]
