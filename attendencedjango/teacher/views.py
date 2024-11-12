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
import datetime
from home.models import Attendance, Subject

def calculate_attendance_percentages_for_students(students, subjects):
    # Dictionary to store attendance percentage for each student by subject
    student_subject_percentages = {}
    start_date_8_months_ago = datetime.date.today() - relativedelta(months=8)
    end_date_today = datetime.date.today()

    for student in students:
        subject_percentages = {}
        for subject in subjects:
            # Get total classes for the student in the given period for the subject
            total_classes_in_period = Attendance.objects.filter(
                student=student,
                subject=subject,
                date__range=[start_date_8_months_ago, end_date_today]
            ).count()

            # Get the number of present classes for the student in the given period for the subject
            present_classes_in_period = Attendance.objects.filter(
                student=student,
                subject=subject,
                status='Present',
                date__range=[start_date_8_months_ago, end_date_today]
            ).count()

            # Calculate percentage
            percentage = int((present_classes_in_period / total_classes_in_period) * 100) if total_classes_in_period > 0 else 0
            
            # Store the percentage in the dictionary
            subject_percentages[subject.id] = percentage

        # Store the subject percentages for each student
        student_subject_percentages[student.id] = subject_percentages

    return student_subject_percentages

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
                context = {'attendance_data': today_attendance, 'date': today}
                
                # Render and create PDF
                pdf_content = render_to_pdf('attendance_today.html', context)
                if pdf_content:
                    filename1 = f"{subject.subjectname.replace(' ', '')}_{today}.pdf"  # Generate filename
                    response = HttpResponse(pdf_content, content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{filename1}"'
                    return response

            elif action == 'download_all':
                filtered_attendance_data = attendance_data.filter(date__range=[eight_months_ago, today])

                distinct_students = filtered_attendance_data.values('student').distinct()
                students = [attendance['student'] for attendance in distinct_students]

                # Calculate attendance percentages for students
                subject_percentages = calculate_attendance_percentages_for_students(students, [subject])
                # Prepare data for the PDF with percentages
                context = {
                 'attendance_data': filtered_attendance_data,
                 'subject': subject,
                 'percentages': subject_percentages, 
                 'date': today if action == 'download_today' else None,
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