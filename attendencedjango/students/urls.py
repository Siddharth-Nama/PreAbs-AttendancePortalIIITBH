from django.contrib import admin
from django.urls import path, include, re_path
from login.views import *
from teacher.views import *
from students.views import *
urlpatterns = [
    # path('attendanceCalender/', attendanceCalender, name='attendanceCalender'),
    # path('get_attendance/', get_attendance, name='get_attendance'),
]