from django.db import models
from django.contrib.auth.models import User
import datetime

# Model for Student
class Student(models.Model):
    name =models.CharField(max_length=100 )
    password = models.CharField(max_length=1000)
    roll_number = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.name} - {self.roll_number}"
    
    def get_attendance_by_subject(self):
        attendance_data = []
        subjects = Subject.objects.all()
        for subject in subjects:
            total_classes = Attendance.objects.filter(subject=subject, student=self).count()
            attended_classes = Attendance.objects.filter(subject=subject, student=self, status='Present').count()
            percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0
            attendance_data.append({
                'subject': subject.subjectname,
                'total_classes': total_classes,
                'attended_classes': attended_classes,
                'percentage': percentage
            })
        return attendance_data
    
    def get_overall_attendance(self):
        total_attendance_data = []
        total_classes = Attendance.objects.filter(student=self).count()
        attended_classes = Attendance.objects.filter(student=self, status='Present').count()
        percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0
        total_attendance_data.append({
            'total_classes': total_classes,
            'attended_classes': attended_classes,
            'percentage': percentage
        })
        return total_attendance_data

# Model for Teacher
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} - {self.user.last_name}"

# Model for Subject
class Subject(models.Model):
    subjectname = models.CharField(max_length=100)
    coursecode = models.CharField(max_length=10, unique=True)
    def get_subject_attendance(self):
        total_classes = Attendance.objects.filter(subject=self).count()
        attended_classes = Attendance.objects.filter(subject=self, status='Present').count()
        total_subject_data = [{
            'total_classes': total_classes,
            'attended_classes': attended_classes,
        }]
        return total_subject_data
    
    def get_present_students(self, date):
        return Student.objects.filter(attendance__subject=self, attendance__date=date, attendance__status='Present')

    def __str__(self):
        return self.subjectname

# Model for Attendance
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.subjectname} - {self.date}"
