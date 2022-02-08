from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views import generic

from .forms import(
    CustomUserCreationForm, 
    PatientModelForm, 
    PatientAssignForm, 
    PatientAppointmentStatusUpdateForm,
)
from .models import Patient, AppointmentStatus
from staff.mixins import OrganiserAndLoginRequiredMixin


class RegisterView(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class HomePageView(generic.TemplateView):
    template_name = 'index.html'


class PatientListView(LoginRequiredMixin, generic.ListView):
    template_name = 'patient_list.html'
    context_object_name = 'patients'
    
    def get_queryset(self):
        user = self.request.user
        # Initial queryset of patients for entire organisation
        if user.is_organiser:
            queryset = Patient.objects.filter(
                organisation=user.userprofile,
                assigned_to__isnull=False,
            )
        else:
            queryset = Patient.objects.filter(
                organisation=user.staffmember.organisation,
                assigned_to__isnull=False,
            )           
            # Filter based on logged in staff member
            queryset = queryset.filter(assigned_to__user=user)    
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Patient.objects.filter(
                organisation=user.userprofile,
                assigned_to__isnull=True,
            )
            context.update({
                'unassigned_patients': queryset 
            })
        return context


class PatientAddView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'patient_add.html'
    form_class = PatientModelForm

    def get_success_url(self):
        return reverse('patients:patient-list')

    def form_valid(self, form):
        patient = form.save(commit=False)
        patient.organisation = self.request.user.userprofile
        patient.save()
        send_mail(
            subject="New patient record added",
            message="Log in to Patient Flow to view the new record.",
            from_email="test@test.co.uk",
            recipient_list=["testuser@test.co.uk"],
        )
        return super().form_valid(form)


class PatientDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'patient_detail.html'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Patient.objects.filter(organisation=user.userprofile)
        else:
            queryset = Patient.objects.filter(organisation=user.staffmember.organisation)
            queryset = queryset.filter(assigned_to__user=user)       
        return queryset
    
    context_object_name = 'patient'


class PatientUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'patient_update.html'
    form_class = PatientModelForm
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Patient.objects.filter(organisation=user.userprofile)
        else:
            queryset = Patient.objects.filter(organisation=user.staffmember.organisation)
            queryset = queryset.filter(assigned_to__user=user)        
        return queryset
    
    def get_success_url(self):
        return reverse('patients:patient-list')


class PatientDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'patient_delete.html'
    queryset = Patient.objects.all()

    def get_success_url(self):
        return reverse('patients:patient-list')


class PatientAssignView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = 'patient_assign.html'
    form_class = PatientAssignForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request,
        })
        return kwargs
   
    def get_success_url(self):
        return reverse('patients:patient-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = Patient.objects.get(id=self.kwargs['pk'])
        context.update({
            'patient': patient 
        })       
        return context

    def form_valid(self, form):
        assigned_to = form.cleaned_data['assigned_to']
        patient = Patient.objects.get(id=self.kwargs['pk'])
        patient.assigned_to=assigned_to
        patient.save()
        return super().form_valid(form)


class AppointmentStatusListView(LoginRequiredMixin, generic.ListView):
    template_name = 'appointment_stats.html'
    context_object_name = 'appointment_stats'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = AppointmentStatus.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = AppointmentStatus.objects.filter(
                organisation=user.staffmember.organisation
            )       
        return queryset

class AppointmentStatusDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'appointment_stat_detail.html'
    context_object_name = 'appointment_stat'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = AppointmentStatus.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = AppointmentStatus.objects.filter(
                organisation=user.staffmember.organisation
            )       
        return queryset

class PatientAppointmentStatusUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'patient_appointment_status_update.html'
    form_class = PatientAppointmentStatusUpdateForm
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Patient.objects.filter(organisation=user.userprofile)
        else:
            queryset = Patient.objects.filter(organisation=user.staffmember.organisation)
            queryset = queryset.filter(assigned_to__user=user)       
        return queryset
    
    def get_success_url(self):
        return reverse('patients:patient-detail', kwargs={'pk': self.get_object().id})
