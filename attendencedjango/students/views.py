from django.shortcuts import render, redirect
from home.models import *
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
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

            # Check if the student has already submitted attendance for this class
            if Attendance.objects.filter(student=student, class_session=session).exists():
                messages.error(request, 'You have already submitted attendance for this class.')
                return redirect('StudentSection')

            # Create a pending attendance request
            Attendance.objects.create(
                student=student,
                subject=session.subject,
                status='Pending',
                date=datetime.date.today(),
                class_session=session
            )
            messages.success(request, 'Attendance request submitted! Awaiting teacher approval.')

        except ClassSession.DoesNotExist:
            messages.error(request, 'Invalid class code!')
        return redirect('StudentSection')

    # Default: Show attendance for today
    today = datetime.date.today()
    attendance_records = Attendance.objects.filter(student=student, date=today)

    # Filters for subject and date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    subject_id = request.GET.get('subject')

    # Filter by date range
    if start_date and end_date:
        attendance_records = Attendance.objects.filter(student=student, date__range=[start_date, end_date])

    # Filter by subject
    if subject_id:
        attendance_records = attendance_records.filter(subject_id=subject_id)

    # Fetch all subjects for filtering dropdown
    subjects = Subject.objects.all()

    # Prepare attendance percentage data
    subject_percentages = {}
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

        percentage = int((present_classes_in_period / total_classes_in_period) * 100) if total_classes_in_period > 0 else 0
        subject_percentages[subject.id] = percentage

    # Attach attendance percentage to each record
    for record in attendance_records:
        record.subject.attendance_percentage = subject_percentages.get(record.subject.id, 0)
   
    total_attended_today = Attendance.objects.filter(student=student, date=timezone.now().date(), status='Present').count()
    total_attendance_today = Attendance.objects.filter(student=student, date=timezone.now().date()).count()
    context = {
        'first_name': request.user.first_name,
        'attendance_records': attendance_records,
        'subjects': subjects,
        'subject_percentages': subject_percentages,
        'total_attended_today':total_attended_today,
        'total_attendance_today':total_attendance_today,
    }

    return render(request, 'studenthomepage.html', context)
