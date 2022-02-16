from django import forms
from django.contrib.auth import get_user_model
from .models import Patient, StaffMember, AppointmentStatus, Priority


User = get_user_model()


class PatientModelForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=StaffMember.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        if user.is_organiser:
            org = user.userprofile
        else:
            org = user.staffmember.organisation
        staff_members = StaffMember.objects.filter(organisation=org)
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


class PatientAppointmentStatusUpdateForm(forms.ModelForm):
    status = forms.ModelChoiceField(queryset=AppointmentStatus.objects.none())
    priority = forms.ModelChoiceField(queryset=Priority.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        if user.is_organiser:
            org = user.userprofile
        else:
            org = user.staffmember.organisation
        statuses = AppointmentStatus.objects.filter(organisation=org).order_by('status')
        priorities = Priority.objects.filter(organisation=org)
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
