from django import forms
from .models import Patient


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
