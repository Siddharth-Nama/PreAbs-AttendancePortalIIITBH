from django.contrib import admin
from .models import *

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
    list_display = ('student', 'subject', 'date', 'status')
    search_fields = ('student__user__username', 'student__roll_number', 'subject__subjectname', 'date')
    list_filter = ('subject', 'status', 'date')

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

# Register the models with the admin site
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(UserProfile)
