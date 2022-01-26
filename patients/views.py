from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Patient
from .forms import PatientModelForm


def home_page(request):
    return HttpResponse("This is the home page")


def patient_list(request):
    patients = Patient.objects.all()
    context = {
        "patients": patients
    }
    return render(request, 'patient_list.html', context)


def patient_detail(request, pk):
    patient = Patient.objects.get(id=pk)
    context = {
        "patient": patient
    }
    return render(request, 'patient_detail.html', context)

def patient_add(request):
    form = PatientModelForm()
    if request.method == "POST":
        form = PatientModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/patients')
    context = {
        "form": PatientModelForm()
    }
    return render(request, 'patient_add.html', context)
