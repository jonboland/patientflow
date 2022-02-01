from django.views import generic
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from patients.models import StaffMember
from .forms import StaffMemberModelForm



class StaffListView(LoginRequiredMixin, generic.ListView):
    template_name = 'staff_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return StaffMember.objects.filter(organisation=organisation)

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


class StaffMemberDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'staff_member_detail.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return StaffMember.objects.filter(organisation=organisation)

    context_object_name = 'staff_member'


class StaffMemberUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'staff_member_update.html'
    form_class = StaffMemberModelForm

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return StaffMember.objects.filter(organisation=organisation)
    
    def get_success_url(self):
        return reverse('staff:staff-list')

    context_object_name = 'staff_member'


class StaffMemberDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'staff_member_delete.html'
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return StaffMember.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('staff:staff-list')
