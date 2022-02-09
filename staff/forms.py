from django import forms
from django.contrib.auth import get_user_model
from patients.models import StaffMember


User = get_user_model()


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class StaffMemberModelForm(forms.ModelForm):

    class Meta:
        model = StaffMember
        fields = (
            'role',
            'notes',
        )
