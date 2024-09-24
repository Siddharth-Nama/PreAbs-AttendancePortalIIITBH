from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from home.models import *

def loginStudent(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        usertype = request.POST.get('usertype')
        print(f"Received email: {email}")
        print(f"Received password: {password}")
        print(f"Received usertype: {usertype}")

        
        try:
            # First, query the User model via email
            user = User.objects.get(email=email)
            user_profile = UserProfile.objects.get(user=user, user_type=usertype)

            # Then check if the user is a student or a teacher
            if usertype == "student":
                student = Student.objects.get(user=user_profile)
            elif usertype == "teacher":
                teacher = Teacher.objects.get(user=user_profile)
            
            # Authenticate using the user's username and password
            user = authenticate(username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid password")
                return redirect('/login/')
        
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist")
            return redirect('/login/')
        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid user type")
            return redirect('/login/')
        except (Student.DoesNotExist, Teacher.DoesNotExist):
            messages.error(request, "No matching student or teacher found")
            return redirect('/login/')

    return render(request, 'login/login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')
