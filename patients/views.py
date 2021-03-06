import logging

from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views import generic
from django.http import Http404

from .forms import PatientModelForm, PatientAppointmentStatusUpdateForm
from .models import Patient, AppointmentStatus
from staff.mixins import OrganiserAndLoginRequiredMixin


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HomePageView(generic.TemplateView):
    template_name = 'index.html'


class PatientListView(LoginRequiredMixin, generic.ListView):
    template_name = 'patient_list.html'
    queryset = Patient.objects.none()

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        if user.is_organiser:
            org = user.userprofile
            assigned = Patient.objects.filter(organisation=org, assigned_to__isnull=False)
            unassigned = Patient.objects.filter(organisation=org, assigned_to__isnull=True)
            context.update({'unassigned_patients': unassigned})
        else:
            org = user.staffmember.organisation
            assigned = Patient.objects.filter(organisation=org, assigned_to__isnull=False)
            assigned = assigned.filter(assigned_to__user=user)
        
        context.update({'assigned_patients': assigned})
        
        status_objects = AppointmentStatus.objects.filter(organisation=org).order_by('status')
        patients_by_status = dict()

        for status_object in status_objects:
            queryset = Patient.objects.filter(organisation=org, status__status=status_object)
            if not user.is_organiser:
                queryset = queryset.filter(assigned_to__user=user)
            patients_by_status[status_object] = queryset

        context.update({'patients_by_status': patients_by_status})

        return context


class PatientAddView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'patient_add.html'
    form_class = PatientModelForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs
    
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
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Patient.objects.filter(organisation=user.userprofile)
        else:
            queryset = Patient.objects.filter(organisation=user.staffmember.organisation)
            queryset = queryset.filter(assigned_to__user=user)        
        return queryset

    def get_success_url(self):
        try:
            return reverse('patients:patient-detail', kwargs={'pk': self.get_object().id})
        except Http404 as ex:
            logger.info(f"{ex},\nPatientUpdateView handled exception type: {type(ex)}")
            return reverse('patients:patient-list')


class PatientDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'patient_delete.html'
    queryset = Patient.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = Patient.objects.get(id=self.kwargs['pk'])
        context.update({
            'patient': patient 
        })       
        return context

    def get_success_url(self):
        return reverse('patients:patient-list')


class AppointmentStatusListView(LoginRequiredMixin, generic.ListView):
    template_name = 'appointment_stats.html'
    queryset = Patient.objects.none()

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        if user.is_organiser:
            org = user.userprofile
        else:
            org = user.staffmember.organisation
        
        status_objects = AppointmentStatus.objects.filter(organisation=org).order_by('status')
        patient_status_counts = dict()

        for status_object in status_objects:
            queryset = Patient.objects.filter(organisation=org, status__status=status_object).count()           
            patient_status_counts[status_object] = queryset

        context.update({'patient_status_counts': patient_status_counts})

        return context


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
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs
    
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
