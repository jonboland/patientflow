from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Patient, StaffMember


User = get_user_model()


class PatientModelForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = (
            'first_name',
            'last_name',
            'age',
            'nhs_number',
            'phone_number',
            'email_address',
            'appointment_needed',
            'priority',
            'notes',
            'assigned_to',
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class PatientAssignForm(forms.Form):
    assigned_to = forms.ModelChoiceField(queryset=StaffMember.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        staff_members = StaffMember.objects.filter(organisation=request.user.userprofile)
        super(PatientAssignForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = staff_members
