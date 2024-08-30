from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class StudentGet(ListAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializers

class TeacherGet(ListAPIView):
    queryset=Teacher.objects.all()
    serializer_class=TeacherSerializers

class SubjectGet(ListAPIView):
    queryset=Subject.objects.all()
    serializer_class=SubjectSerializers

class AttendanceGet(ListAPIView):
    queryset=Attendance.objects.all()
    serializer_class=AttendanceSerializers

class StudentPost(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializers

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        password = request.data.get('password')
        roll_number = request.data.get('roll_number')

        if not roll_number:
            return Response({"error": "Roll number is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        student = Student.objects.create(
            name=name,
            roll_number=roll_number
        )
        student.save()
        
        serializer = self.get_serializer(student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class TeacherPost(CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializers

    def post(self, request, *args, **kwargs):
        user = request.user

        teacher = Teacher.objects.create(
            user=user,
        )
        teacher.save()
        
        serializer = self.get_serializer(teacher)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class SubjectPost(CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializers

    def post(self, request, *args, **kwargs):
        subjectname = request.data.get('subjectname')
        coursecode = request.data.get('coursecode')

        if not subjectname or not coursecode:
            return Response({"error": "Subject name and course code are required."}, status=status.HTTP_400_BAD_REQUEST)

        subject = Subject.objects.create(
            subjectname=subjectname,
            coursecode=coursecode
        )
        subject.save()
        
        serializer = self.get_serializer(subject)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AttendancePost(CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializers
    
    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student')
        subject_id = request.data.get('subject')
        date = request.data.get('date')
        status = request.data.get('status')
        
        if not student_id or not subject_id or not date or not status:
            return Response({"error": "Student, subject, date, and status are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id)
            subject = Subject.objects.get(id=subject_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found."}, status=status.HTTP_400_BAD_REQUEST)

        attendance = Attendance.objects.create(
            student=student,
            subject=subject,
            date=date,
            status=status
        )
        attendance.save()
        
        serializer = self.get_serializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
