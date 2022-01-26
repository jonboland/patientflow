from django.urls import path
from .views import patient_list, patient_detail

app_name = 'patients'

urlpatterns = [
    path('', patient_list),
    path('<pk>/', patient_detail),
]
