from django.shortcuts import render, redirect
from home.models import *
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.

@login_required(login_url="/accounts/login/")
def StudentSection(request):
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
    
    context = {
        'first_name': request.user.first_name,
    }   

    return render(request, 'studenthomepage.html',context)
