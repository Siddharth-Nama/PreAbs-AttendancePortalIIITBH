from rest_framework import serializers
from .models import *

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class AttendanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

