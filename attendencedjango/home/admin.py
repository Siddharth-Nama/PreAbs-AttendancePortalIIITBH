from django.contrib import admin
from .models import *
from datetime import datetime
from django.db.models import Q
from django.utils.html import format_html


# ModelAdmin for Subject
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subjectname', 'coursecode')  
    search_fields = ('subjectname', 'coursecode')
    list_filter = ('subjectname', 'coursecode')

# ModelAdmin for Student
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'roll_number', 'get_first_name', 'get_last_name')
    search_fields = ('user__user__username', 'roll_number', 'user__user__first_name', 'user__user__last_name')
    list_filter = ('roll_number', 'user__user__first_name', 'user__user__last_name')
    def get_username(self, obj):
        return obj.user.user.username
    get_username.admin_order_field = 'user__user__username'
    get_username.short_description = 'Username'

    def get_first_name(self, obj):
        return obj.user.user.first_name
    get_first_name.admin_order_field = 'user__user__first_name'
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.user.last_name
    get_last_name.admin_order_field = 'user__user__last_name'
    get_last_name.short_description = 'Last Name'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')
    
# ModelAdmin for Attendance
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'student', 
        'get_class_session_code',  
        'subject', 
        'date', 
        'status'
    )
    
    search_fields = (
        'student__roll_number',
        'subject__subjectname',
        'date',
        'class_session__code', 
    )
    
    list_filter = ('subject', 'status', 'date', 'class_session') 

    def get_class_session_code(self, obj):
        return obj.class_session.code if obj.class_session else 'N/A'
    get_class_session_code.short_description = 'Class Session Code'

# ModelAdmin for Teacher
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name')
    search_fields = ('user__user__username', 'user__user__first_name', 'user__user__last_name')
    list_filter = ('user__user__first_name', 'user__user__last_name')

    def get_first_name(self, obj):
        return obj.user.user.first_name
    get_first_name.admin_order_field = 'user__user__first_name'
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.user.last_name
    get_last_name.admin_order_field = 'user__user__last_name'
    get_last_name.short_description = 'Last Name'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')

# ModelAdmin for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'user_type', 'get_first_name', 'get_last_name')
    search_fields = ('user__username', 'user_type', 'user__first_name', 'user__last_name')
    list_filter = ('user_type',)

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user__username'
    get_username.short_description = 'Username'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'
    get_last_name.short_description = 'Last Name'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')



class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ('code', 'subject', 'teacher', 'created_at', 'expires_at')
    list_filter = ('subject', 'teacher', 'created_at', 'expires_at')
    search_fields = ('subject__subjectname', 'teacher__user__user__first_name', 'teacher__user__user__last_name', 'code', 'created_at')    

# Register the models with the admin site
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(ClassSession,ClassSessionAdmin)
