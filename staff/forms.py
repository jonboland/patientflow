from django import forms
from django.contrib.auth import get_user_model
from patients.models import StaffMember, Role


User = get_user_model()


class UserModelForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

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
