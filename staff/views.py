import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse
from django.views import generic
from patients.models import StaffMember

from .forms import StaffMemberModelForm, UserModelForm
from .mixins import OrganiserAndLoginRequiredMixin
from .decorators import login_and_organiser_required


User = get_user_model()


class StaffListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = 'staff_list.html'
    context_object_name = 'staff'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return StaffMember.objects.filter(organisation=organisation)
    

@login_and_organiser_required
def staff_member_add(request):
    
    user_form = UserModelForm()
    staff_member_form = StaffMemberModelForm()

    if request.method == "POST":
        user_form = UserModelForm(request.POST)
        staff_member_form = StaffMemberModelForm(request.POST)        
        
        if user_form.is_valid() and staff_member_form.is_valid():            
            user = user_form.save(commit=False)
            user.is_staff_member = True
            user.is_organiser = False
            password = ''.join(random.choice(string.ascii_letters) for x in range(10))
            user.set_password(password)
            user.save()           
            staff_member = staff_member_form.save(commit=False)
            staff_member.user = user
            staff_member.organisation = request.user.userprofile          
            staff_member.save()

            send_mail(
                subject='Patient Flow Invite',
                message=(
                    'You have been added to Patient Flow '
                    'and can now login to begin picking up referrals.'
                ),
                from_email='admin@patientflow.co.uk',
                recipient_list=[user.email],
            )
            
            return redirect('staff:staff-list')

    context = {
        'user_form': user_form,
        'staff_member_form': staff_member_form,
    }

    return render(request, 'staff_member_add.html', context)


class StaffMemberDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = 'staff_member_detail.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return StaffMember.objects.filter(organisation=organisation)

    context_object_name = 'staff_member'


@login_and_organiser_required
def staff_member_update(request, pk):
    
    organisation = request.user.userprofile

    staff_member = StaffMember.objects.get(id=pk, organisation=organisation) 
    staff_member_form = StaffMemberModelForm(instance=staff_member)

    user = User.objects.get(id=staff_member.user_id)
    user_form = UserModelForm(instance=user)
    
    if request.method == 'POST':
        user_form = UserModelForm(request.POST, instance=user)
        staff_member_form = StaffMemberModelForm(request.POST, instance=staff_member)
        if user_form.is_valid() and staff_member_form.is_valid():
            user_form.save()
            staff_member_form.save()
            
            return redirect('/staff')

    context = {
        'user': user,
        'user_form': user_form,
        'staff_member': staff_member,
        'staff_member_form': staff_member_form,
    }

    return render(request, 'staff_member_update.html', context)


class StaffMemberDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'staff_member_delete.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return StaffMember.objects.filter(organisation=organisation)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_member = StaffMember.objects.get(id=self.kwargs['pk'])
        context.update({
            'staff_member': staff_member 
        })       
        return context

    def get_success_url(self):
        return reverse('staff:staff-list')
