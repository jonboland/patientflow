from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient


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
