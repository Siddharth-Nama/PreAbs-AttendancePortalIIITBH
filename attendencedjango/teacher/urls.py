from django.contrib import admin
from django.urls import path, include, re_path
from login.views import *
from teacher.views import *
from students.views import *
urlpatterns = [
    path('attendanceSubject/', attendanceSubject, name="attendanceSubject")
]