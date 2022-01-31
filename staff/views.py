from django.views import generic
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from patients.models import StaffMember
from .forms import StaffMemberModelForm



class StaffListView(LoginRequiredMixin, generic.ListView):
    template_name = 'staff_list.html'

    def get_queryset(self):
        return StaffMember.objects.all()

    context_object_name = 'staff'


class StaffMemberAddView(LoginRequiredMixin, generic.CreateView):
    template_name = 'staff_member_add.html'
    form_class = StaffMemberModelForm

    def get_success_url(self):
        return reverse('staff:staff-list')

    def form_valid(self, form):
        staff_member = form.save(commit=False)
        staff_member.organisation = self.request.user.userprofile
        staff_member.save()
        return super(StaffMemberAddView, self).form_valid(form)
