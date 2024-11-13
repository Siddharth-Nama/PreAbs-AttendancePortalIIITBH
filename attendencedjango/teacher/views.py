from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from home.models import *
import random
import string
from datetime import datetime, timedelta
import datetime
from django.utils import timezone
from django.views.decorators.cache import never_cache
import pandas as pd  # For handling data and exporting to PDF or other formats
from django.template.loader import get_template
from weasyprint import HTML
from django_renderpdf.views import PDFView
from io import BytesIO
from xhtml2pdf import pisa
from dateutil.relativedelta import relativedelta
from collections import defaultdict

def calculate_attendance_percentages_for_students(roll_numbers, subjects):
    # Dictionary to store percentages for each student and subject
    attendance_percentages = defaultdict(lambda: defaultdict(int))

    # Loop over each student
    for roll_number in roll_numbers:
        # Filter attendance records for the specific student and subjects
        student_attendance_records = Attendance.objects.filter(
            student__roll_number=roll_number,
            subject__in=subjects
        )

        # Calculate attendance percentage for each subject
        for subject in subjects:
            total_classes = student_attendance_records.filter(subject=subject).count()
            present_classes = student_attendance_records.filter(subject=subject, status="Present").count()
            print("Total ------------------> ",total_classes)
            print("Present ------------------> ",present_classes)
            # Calculate percentage only if total classes are greater than zero to avoid division by zero
            if total_classes > 0:
                attendance_percentage = (present_classes / total_classes) * 100
            else:
                attendance_percentage = 0

            # Store the result in the dictionary
            attendance_percentages[roll_number][subject.coursecode] = round(attendance_percentage, 2)

    return attendance_percentages


@never_cache
@login_required
def TeacherSection(request):
    subjects = Subject.objects.all()
    context = {
        'first_name': request.user.first_name,
        'subjects': subjects,  
    }
    return render(request, 'teacherhomepage.html', context)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None



@never_cache
@login_required
def download_attendance(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        attendance_class = request.POST.get('attendance_class')

        try:
            subject = Subject.objects.get(coursecode=attendance_class)  # Fetch subject based on course code
        except Subject.DoesNotExist:
            messages.error(request, "Subject with the given course code does not exist.")
            return redirect('TeacherSection')
        
        today = datetime.datetime.today().date() 
        current_year = today.year

        if attendance_class != '0':
            attendance_data = Attendance.objects.filter(subject__coursecode=attendance_class)
            eight_months_ago = today - timedelta(days=8 * 30)
            
            if action == 'download_today':
                today_attendance = attendance_data.filter(date=today)
                
                # Get distinct roll numbers with attendance status for today
                distinct_students = today_attendance.values(
                    'student__roll_number', 
                    'student__user__user__first_name', 
                    'student__user__user__last_name',
                    'status'
                ).distinct()

                unique_students = [
                    {
                        'roll_number': student['student__roll_number'],
                        'first_name': student['student__user__user__first_name'],
                        'last_name': student['student__user__user__last_name'],
                        'status': student['status']  # Fetch status for today
                    }
                    for student in distinct_students
                ]
                
                context = {
                    'attendance_data': unique_students,
                    'date': today,
                    'subject':subject
                }
                print("Today's Attendance Data:", context)
                # Render and create PDF
                pdf_content = render_to_pdf('attendance_today.html', context)
                if pdf_content:
                    filename1 = f"{subject.subjectname.replace(' ', '')}_{today}.pdf"  # Generate filename
                    response = HttpResponse(pdf_content, content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{filename1}"'
                    return response

            elif action == 'download_all':
                filtered_attendance_data = attendance_data.filter(date__range=[eight_months_ago, today])

                # Get distinct roll numbers with student details
                distinct_students = filtered_attendance_data.values(
                    'student__roll_number', 'student__user__user__first_name', 'student__user__user__last_name'
                ).distinct()

                unique_students = [
                    {
                        'roll_number': student['student__roll_number'],
                        'first_name': student['student__user__user__first_name'],
                        'last_name': student['student__user__user__last_name']
                    }
                    for student in distinct_students
                ]

                # Calculate attendance percentages for each unique student and subject
                roll_numbers = [student['roll_number'] for student in unique_students]
                subject_percentages = calculate_attendance_percentages_for_students(roll_numbers, [subject])

                # Add attendance percentage to each student's data
                attendance_data_with_percentages = [
                    {
                        'roll_number': student['roll_number'],
                        'first_name': student['first_name'],
                        'last_name': student['last_name'],
                        'percentage': subject_percentages.get(student['roll_number'], {}).get(subject.coursecode, 0)
                    }
                    for student in unique_students
                ]
                # print("Attendance ----------------------> ",attendance_data_with_percentages)
                context = {
                    'attendance_data': attendance_data_with_percentages,  # Includes student details and attendance percentage
                    'subject': subject,
                    'start_date': eight_months_ago,
                    'end_date': today,
                }
                
                # Render and create PDF
                pdf_content = render_to_pdf('attendance_all.html', context)
                if pdf_content:
                    filename = f"{subject.subjectname.replace(' ', '')}_{current_year}.pdf"  # Generate filename
                    response = HttpResponse(pdf_content, content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                    return response

        else:
            messages.error(request, "Please select a valid subject.")
            return redirect('TeacherSection')

    return redirect('TeacherSection')

def generate_unique_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase , k=6))
        if not ClassSession.objects.filter(code=code).exists():
            print("code----------------------->", code)
            return code

@never_cache
@login_required
def attendanceSubject(request):
    if request.method == "POST":
        coursecode = request.POST.get("class")

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

        pending_students = Attendance.objects.filter(status='Pending', class_session__code=unique_code)

        unique_students = {}
        for attendance in pending_students:
            if attendance.student.id not in unique_students:
                unique_students[attendance.student.id] = {
                    'user': attendance.student.user,
                    'roll_number': attendance.student.roll_number,
                }

        # Convert unique_students dictionary to a list
        students = list(unique_students.values())

        return render(request, 'attendencePageforTeacher.html', {
            'subjectname': subjectname,
            'coursecode': coursecode,
            'unique_code': unique_code,  
            'expiry_time': expiry_time,
            'pendingStudents': students,
        })
    
    subjects = Subject.objects.all()
    return render(request, 'attendencePageforTeacher.html', {'subjects': subjects})

@never_cache
def submit_attendance(request):
    status = request.POST.get("attendance_radio")
    unique_code = request.POST.get('unique_code')
    pending_students = Attendance.objects.filter(status='Pending', class_session__code=unique_code)

    if status == 'Allpresent':
        for attendance in pending_students:
            attendance.status = 'Present'
            attendance.save()
    else:
        
        for attendance in pending_students:
            if status == 'present':
                attendance.status = 'Present'
            elif status == 'absent':
                attendance.status = 'Absent'
            attendance.save()

    return redirect('TeacherSection')