from django.contrib import admin

from django.utils.translation import gettext_lazy as _

# Customize admin site header and title
admin.site.site_header = _("IIITBH Attendance Portal")
admin.site.site_title = _("IIITBH Attendance Portal Admin")
admin.site.index_title = _("Welcome to the IIITBH Attendance Portal Admin Dashboard")
