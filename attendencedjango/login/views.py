from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from home.models import *

def loginStudent(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        password = request.POST.get('password')
        print(f"Received roll_number: {roll_number}")
        print(f"Received password: {password}")

        try:
            student = Student.objects.get(roll_number=roll_number)
            user = student.user
            user = authenticate(username=user.user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid password")
                return redirect('/login/student')
        except Student.DoesNotExist:
            messages.error(request, "Invalid roll number")
            return redirect('/login/student')

    return render(request, 'login/login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')
