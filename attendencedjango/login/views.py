from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from home.models import *
from django.views.decorators.cache import never_cache

@never_cache
def home(request):
    return redirect('/accounts/login/')

@never_cache
def loginStudent(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        usertype = request.POST.get('usertype')
        print(f"Received email: {email}")
        print(f"Received password: {password}")
        print(f"Received usertype: {usertype}")

        try:
            user = User.objects.get(email=email)
            user_profile = UserProfile.objects.get(user=user, user_type=usertype)

            user = authenticate(username=user.username, password=password)

            if user is not None:
                login(request, user)

                if usertype == "student":
                    return redirect('/StudentSection/')
                elif usertype == "teacher":
                    return redirect('/TeacherSection/')
            else:
                messages.error(request, "Invalid password")
                return redirect('/accounts/login/')

        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist")
            return redirect('/accounts/login/')
        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid user type")
            return redirect('/accounts/login/')
        except (Student.DoesNotExist, Teacher.DoesNotExist):
            messages.error(request, "No matching student or teacher found")
            return redirect('/accounts/login/')

    return render(request, 'login/login.html')

@never_cache
def logout_page(request):
    logout(request)
    return redirect('/accounts/login/')

@never_cache
def newRegistration(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        roll_number = request.POST.get('rollno')
        mobile = request.POST.get('mobile')

        # Validate username
        if not username:
            messages.error(request, "Username is required")
            return redirect('/newRegistration/')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect('/newRegistration/')

        # Check if the roll number already exists in the Student model
        if Student.objects.filter(roll_number=roll_number).exists():
            messages.info(request, "Roll Number already taken")
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
            user_type='student'  # Assuming it's a student registration
        )

        # Create the Student profile linked to the UserProfile
        student = Student.objects.create(
            user=user_profile,  # Linked to UserProfile, not User directly
            roll_number=roll_number,
            mobile=mobile,
            image=None  # You can update this to handle image uploads later
        )

        # Save both models
        user_profile.save()
        student.save()

        messages.info(request, "Account created successfully")
        return redirect('/accounts/login/')

    return render(request, 'login/register.html')
