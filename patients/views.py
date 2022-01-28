from django.core.mail import send_mail
from django.shortcuts import reverse
from django.views import generic
from .forms import PatientModelForm, CustomUserCreationForm
from .models import Patient


class RegisterView(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class HomePageView(generic.TemplateView):
    template_name = 'index.html'


class PatientListView(generic.ListView):
    template_name = 'patient_list.html'
    queryset = Patient.objects.all()
    context_object_name = 'patients'


class PatientDetailView(generic.DetailView):
    template_name = 'patient_detail.html'
    queryset = Patient.objects.all()
    context_object_name = 'patient'


class PatientAddView(generic.CreateView):
    template_name = 'patient_add.html'
    form_class = PatientModelForm

    def get_success_url(self):
        return reverse('patients:patient-list')

    def form_valid(self, form):
        send_mail(
            subject="New patient record added",
            message="Log in to Patient Flow to view the new record.",
            from_email="test@test.co.uk",
            recipient_list=["testuser@test.co.uk"],
        )
        return super(PatientAddView, self).form_valid(form)


class PatientUpdateView(generic.UpdateView):
    template_name = 'patient_update.html'
    queryset = Patient.objects.all()
    form_class = PatientModelForm

    def get_success_url(self):
        return reverse('patients:patient-list')


class PatientDeleteView(generic.DeleteView):
    template_name = 'patient_delete.html'
    queryset = Patient.objects.all()

    def get_success_url(self):
        return reverse('patients:patient-list')
