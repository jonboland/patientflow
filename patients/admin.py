from django.contrib import admin

from .models import User, Patient, StaffMember, UserProfile, AppointmentStatus


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Patient)
admin.site.register(StaffMember)
admin.site.register(AppointmentStatus)
