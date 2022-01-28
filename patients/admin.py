from django.contrib import admin

from .models import User, Patient, StaffMember, UserProfile


admin.site.register(User)
admin.site.register(Patient)
admin.site.register(StaffMember)
admin.site.register(UserProfile)
