from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import Subject
import qrcode
from io import BytesIO
import base64
import time

@login_required
def TeacherSection(request):
    subjects = Subject.objects.all()
    context = {
        'first_name': request.user.first_name,
        'subjects': subjects,  
    }
    return render(request, 'teacherhomepage.html', context)

def generate_qr_code(coursecode, subjectname, expiry_time_seconds):
    # Get the current timestamp
    current_time = int(time.time())

    # QR code data with an expiry timestamp
    qr_data = f"{coursecode}:{subjectname}:{current_time + expiry_time_seconds}"

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill="black", back_color="white")

    # Save the QR code as an image in memory
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Convert the image to base64 for display in the template
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return qr_code_base64


@login_required
def attendanceSubject(request):
    if request.method == "POST":
        coursecode = request.POST.get("class")

        # Validate if the user has selected a subject
        if coursecode == '0':
            subjects = Subject.objects.all()
            messages.error(request, "Please select a valid subject.")
            return render(request, 'teacherhomepage.html', {
                'subjects': subjects,
            })

        # Fetch the subject by course code
        try:
            subject = Subject.objects.get(coursecode=coursecode)
            subjectname = subject.subjectname
        except Subject.DoesNotExist:
            messages.error(request, "Invalid subject selection.")
            return redirect('TeacherSection')

        # Set the expiry time for the QR code (e.g., 60 minutes = 3600 seconds)
        expiry_time_seconds = 3600  # 60 minutes
        qr_code = generate_qr_code(coursecode, subjectname, expiry_time_seconds)

        # Pass the QR code to the template
        return render(request, 'QRattendance.html', {
            'subjectname': subjectname,
            'coursecode': coursecode,
            'qr_code': qr_code,
        })
