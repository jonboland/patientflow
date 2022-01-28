from django.shortcuts import reverse
from django.views import generic
from .forms import PatientModelForm
from .models import Patient


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
