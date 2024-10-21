from django.shortcuts import render, redirect
from home.models import *
from django.http import JsonResponse
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.
from django.views.decorators.cache import never_cache
from dateutil.relativedelta import relativedelta    

@never_cache
@login_required(login_url="/accounts/login/")
def StudentSection(request):
    student = request.user.userprofile.student
    if request.method == 'POST':
        code = request.POST.get('class_code')

        try:
            session = ClassSession.objects.get(code=code)

            # Check if session is expired
            if session.expires_at < timezone.now():
                messages.error(request, 'This class session code has expired.')
                return redirect('submit_code')

            student = request.user.userprofile.student
            class_session = ClassSession.objects.get(code=code)
            
            # Check if the student is already present in this class session
            if Attendance.objects.filter(student=student, class_session=class_session).exists():
                messages.error(request, 'You have already submitted attendance for this class.')
                return redirect('StudentSection')

            # Create a pending attendance request
            Attendance.objects.create(
                student=student,
                subject=session.subject,
                status='Pending',  # Set status as Pending
                date=datetime.date.today(),
                class_session=class_session  # Use the retrieved class session
              )
            messages.success(request, 'Attendance request submitted! Awaiting teacher approval.')

        except ClassSession.DoesNotExist:
            messages.error(request, 'Invalid class code!')

        return redirect('StudentSection')
     # Default: Filter attendance for today
    today = datetime.date.today()
    attendance_records = Attendance.objects.filter(student=student, date=today)

    # Get filters from the request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    subject_id = request.GET.get('subject')

    # Filter by date range if provided
    if start_date and end_date:
        attendance_records = Attendance.objects.filter(student=student, date__range=[start_date, end_date])

    # Filter by subject if provided
    if subject_id:
        attendance_records = attendance_records.filter(subject_id=subject_id)

    # Count total classes attended today
    total_classes_attended_today = attendance_records.filter(status='Present').count()
    total_classes_today = attendance_records.count()

    # Fetch all subjects for the dropdown filter
    subjects = Subject.objects.all()
    
    # Prepare a dictionary to hold attendance percentages for each subject
    subject_percentages = {}
    
    # Calculate total attendance percentages for each subject
    start_date_8_months_ago = datetime.date.today() - relativedelta(months=8)
    end_date_today = datetime.date.today()

    for subject in subjects:
        total_classes_in_period = Attendance.objects.filter(
            student=student, 
            subject=subject, 
            date__range=[start_date_8_months_ago, end_date_today]
        ).count()

        present_classes_in_period = Attendance.objects.filter(
            student=student, 
            subject=subject, 
            status='Present',
            date__range=[start_date_8_months_ago, end_date_today]
        ).count()

        if total_classes_in_period > 0:
            percentage = int((present_classes_in_period / total_classes_in_period) * 100)
        else:
            percentage = 0
            
        subject_percentages[subject.id] = percentage

    # Attach the attendance percentage to each attendance record
    for record in attendance_records:
        record.subject.attendance_percentage = subject_percentages.get(record.subject.id, 0)

    context = {
        'first_name': request.user.first_name,
        'attendance_records': attendance_records,
        'total_attendance_today': total_classes_today,
        'total_attended_today': total_classes_attended_today,
        'subjects': subjects,
        'subject_percentages': subject_percentages,
        'date': record.date.strftime('%Y-%m-%d'),
        'status': record.status 
    }  

    return render(request, 'studenthomepage.html',context)

def attendanceCalender(request):
    
    context={}

    return render(request, 'attendanceCalender.html',context)



@login_required(login_url="/accounts/login/")
def get_attendance(request):
    student = request.user.userprofile.student
    coursecode = request.GET.get('subject')
    
    # Fetch attendance records for the selected subject
    attendance_records = Attendance.objects.filter(
        student=student,
        subject__coursecode=coursecode
    )

    # Format the data to be JSON friendly
    attendance_data = [
        {
            'date': record.date.strftime('%Y-%m-%d'),
            'status': record.status  # 'Present', 'Absent', 'Pending'
        }
        for record in attendance_records
    ]

    return redirect(request, attendance_data)