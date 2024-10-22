from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from home.models import *
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.cache import never_cache
import pandas as pd  # For handling data and exporting to PDF or other formats
from django.template.loader import get_template
from weasyprint import HTML
from django_renderpdf.views import PDFView
from django.core.files.base import ContentFile
from io import BytesIO
from xhtml2pdf import pisa

@never_cache
@login_required
def TeacherSection(request):
    subjects = Subject.objects.all()
    context = {
        'first_name': request.user.first_name,
        'subjects': subjects,  
    }
    return render(request, 'teacherhomepage.html', context)

class AttendancePDFView(PDFView):
    template_name = 'attendance_today.html'  # Template for today's attendance

    def get_context_data(self, *args, **kwargs):
        attendance_data = kwargs.get('attendance_data', [])
        date = kwargs.get('date')
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'attendance_data': attendance_data,
            'date': date,
        })
        return context

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

@never_cache
@login_required
def download_attendance(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        attendance_class = request.POST.get('attendance_class')

        if attendance_class != '0':
            # Fetch attendance data based on the selected class
            attendance_data = Attendance.objects.filter(subject__coursecode=attendance_class)
            # Calculate date range
            today = datetime.today().date()
            eight_months_ago = today - timedelta(days=8*30)  # Approximate 8 month

            if action == 'download_today':
                today = datetime.today().date()
                today_attendance = attendance_data.filter(date=today)

                # Generate PDF for today's attendance
                response = AttendancePDFView.as_view()(request, attendance_data=today_attendance, date=today)
                response['Content-Disposition'] = 'attachment; filename="today_attendance.pdf"'
                return response

            elif action == 'download_all':
                # Filter attendance data for the date range
                filtered_attendance_data = attendance_data.filter(date__range=[eight_months_ago, today])

                # Create a PDF report for all attendance in the specified date range
                template = get_template('attendance_all.html')  # Ensure this template exists
                context = {'attendance_data': filtered_attendance_data, 'start_date': eight_months_ago, 'end_date': today}
                html = template.render(context)


                pdf_file = HTML(string=html).write_pdf()

                # Generate PDF and return it as a response
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="all_attendance.pdf"'

                # Generate PDF
                response.write(pdf_file)
                return response

        else:
            subjects = Subject.objects.all()
            messages.error(request, "Please select a valid subject.")
            return redirect('TeacherSection')

        # Redirect back to the TeacherSection if no valid class is selected
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