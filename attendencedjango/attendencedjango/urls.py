from django.contrib import admin
from django.urls import path, include
from login.views import loginStudent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('home.urls')),  
    path('login/student/', loginStudent, name="login"), 
]
