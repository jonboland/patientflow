from django.urls import path
from .views import (
    patient_list, patient_detail, patient_add, patient_update, patient_delete
)


app_name = 'patients'

urlpatterns = [
    path('', patient_list, name='patient-list'),
    path('<int:pk>/', patient_detail, name='patient-detail'),
    path('<int:pk>/update/', patient_update, name='patient-update'),
    path('<int:pk>/delete/', patient_delete, name='patient-delete'),
    path('add/', patient_add, name='patient-add'),
]
