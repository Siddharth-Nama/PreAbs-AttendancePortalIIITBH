from django.urls import path
from home.views import *
urlpatterns = [
    path('StudentGet/',StudentGet.as_view()),
    path('TeacherGet/',TeacherGet.as_view()),
    path('SubjectGet/',SubjectGet.as_view()),
    path('AttendanceGet/',AttendanceGet.as_view()),
    path('StudentPost/',StudentPost.as_view()),
    path('TeacherPost/',TeacherPost.as_view()),
    path('SubjectPost/',SubjectPost.as_view()),
    path('AttendancePost/',AttendancePost.as_view()),
    
]
