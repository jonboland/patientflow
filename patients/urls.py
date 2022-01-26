from django.urls import path
from .views import patient_list, patient_detail, patient_add

app_name = 'patients'

urlpatterns = [
    path('', patient_list),
    path('<int:pk>/', patient_detail),
    path('add/', patient_add),
]
