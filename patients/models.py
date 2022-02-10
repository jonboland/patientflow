from distutils.command.build_scripts import first_line_re
from statistics import mode
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


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
    notes = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        'StaffMember', blank=True, null=True, on_delete=models.SET_NULL
    )
    status = models.ForeignKey(
        'AppointmentStatus', related_name='patients', blank=True, null=True, on_delete=models.SET_NULL
    )
    priority = models.ForeignKey(
        'Priority', related_name='patients', blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.age}, {self.nhs_number}"


class StaffMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(
        'Role', related_name='staff_members', blank=True, null=True, on_delete=models.SET_NULL
    )
    notes = models.TextField(blank=True)  

    def __str__(self):
        return f"{self.role} {self.user.first_name} {self.user.last_name}"


class AppointmentStatus(models.Model):
    status = models.CharField(max_length=50)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = 'statuses'


class Role(models.Model):
    role = models.CharField(max_length=50)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.role


class Priority(models.Model):
    priority = models.CharField(max_length=50)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.priority

    class Meta:
        verbose_name_plural = 'priorities'


def post_user_added_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_added_signal, sender=User)
