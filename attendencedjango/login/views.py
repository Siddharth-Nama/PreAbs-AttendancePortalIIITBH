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


def newRegistration(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        roll_number = request.POST.get('rollno') 
        mobile = request.POST.get('mobile')
        if not username:
            messages.error(request, "Username is required")
            return redirect('/newRegistration/')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect('/newRegistration/')

        # Create the User object
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Create the UserProfile linked to the user
        user_profile = UserProfile.objects.create(
            user=user,
            user_type='student' 
        )

        # Create the Student profile 
        student = Student.objects.create(
            user=user_profile,  # Linked to UserProfile, not User
            roll_number=roll_number,  
            mobile=mobile,
            image=None  
        )

        # Save both models
        user_profile.save()
        student.save()

        messages.info(request, "Account created successfully")
        return redirect('/login/')

    return render(request, 'login/register.html')