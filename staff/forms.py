from django import forms
from django.contrib.auth import get_user_model
from patients.models import StaffMember, Role


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
    def __init__(self, *args, **kwargs):
        organisation = kwargs.pop('organisation')
        roles = Role.objects.filter(organisation=organisation)
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = roles

    class Meta:
        model = StaffMember
        fields = (
            'role',
            'notes',
        )
