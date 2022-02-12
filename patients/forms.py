from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Patient, StaffMember, AppointmentStatus, Priority


User = get_user_model()


class PatientModelForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=StaffMember.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        staff_members = StaffMember.objects.filter(organisation=request.user.userprofile)
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = staff_members
        self.fields['assigned_to'].required = False

    class Meta:
        model = Patient
        fields = (
            'first_name',
            'last_name',
            'age',
            'nhs_number',
            'phone_number',
            'email_address',
            'assigned_to',
            'notes',
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class PatientAppointmentStatusUpdateForm(forms.ModelForm):
    status = forms.ModelChoiceField(queryset=AppointmentStatus.objects.none())
    priority = forms.ModelChoiceField(queryset=Priority.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        organisation = request.user.userprofile
        statuses = AppointmentStatus.objects.filter(organisation=organisation)
        priorities = Priority.objects.filter(organisation=organisation)
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = statuses
        self.fields['status'].required = False
        self.fields['priority'].queryset = priorities
        self.fields['priority'].required = False

    class Meta:
        model = Patient
        fields = (
            'status',
            'priority',
        )
