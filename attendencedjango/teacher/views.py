from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/accounts/login/")
def TeacherSection(request):
    
    return render(request,'teacherhomepage.html')