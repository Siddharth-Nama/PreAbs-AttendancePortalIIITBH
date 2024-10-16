from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import *
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone

@login_required
def TeacherSection(request):
    subjects = Subject.objects.all()
    context = {
        'first_name': request.user.first_name,
        'subjects': subjects,  
    }
    return render(request, 'teacherhomepage.html', context)

def generate_unique_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase , k=6))
        if not ClassSession.objects.filter(code=code).exists():
            print("code----------------------->", code)
            return code

@login_required
def attendanceSubject(request):
    if request.method == "POST":
        coursecode = request.POST.get("class")
        alert_message = None
        expiry_time = None
        unique_code = None  
        subjectname = None
        if coursecode == '0':
            subjects = Subject.objects.all()
            messages.error(request, "Please select a valid subject.")
            return redirect('TeacherSection')

        try:
            subject = Subject.objects.get(coursecode=coursecode)
            subjectname = subject.subjectname
        except Subject.DoesNotExist:
            messages.error(request, "Invalid subject selection.")
            return redirect('TeacherSection')

        # Get current time
        current_time = timezone.now()

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            teacher = Teacher.objects.get(user=user_profile)        
        except Teacher.DoesNotExist:
            messages.error(request, "Teacher account not found.")
            return redirect('TeacherSection')

        # Check if there is an existing active session
        existing_session = ClassSession.objects.filter(
            subject=subject, 
            teacher=teacher,
            expires_at__gt=current_time 
        ).first()

        if existing_session:
            # If an active session exists, return the existing code
            unique_code = existing_session.code
            alert_message = 'An active session already exists for this subject.'
        else:
            # No active session, generate a new code
            unique_code = generate_unique_code()

            # Calculate expiry time (e.g., 1 hour from now)
            expiry_time = current_time + timedelta(hours=1)

            # Create a new class session
            class_session = ClassSession.objects.create(
                subject=subject,
                teacher=teacher,
                code=unique_code,
                expires_at=expiry_time
            )
        return render(request, 'attendencePageforTeacher.html', {
            'subjectname': subjectname,
            'coursecode': coursecode,
            'unique_code': unique_code,  
            'alert_message': alert_message, 
            'expiry_time': expiry_time,
        })
