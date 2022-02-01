from distutils.command.build_scripts import first_line_re
from statistics import mode
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


PRIORITIES = (
    ('L', 'Low'),
    ('M', 'Medium'),
    ('H', 'High'),
)

ROLES = (
    ('GP', 'GP'),
    ('Nurse', 'Nurse'),
)


class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_staff_member = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    nhs_number = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    appointment_needed = models.BooleanField(default=False)
    priority = models.CharField(choices=PRIORITIES, max_length=6, blank=True)
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        'StaffMember', blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.age}, {self.nhs_number}"


class StaffMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES, max_length=50)    

    def __str__(self):
        return f"{self.role} {self.user.first_name} {self.user.last_name}"


def post_user_added_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_added_signal, sender=User)
