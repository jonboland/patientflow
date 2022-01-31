from django import forms
from patients.models import StaffMember


class StaffMemberModelForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = (
            'user',
            'role',
        )
