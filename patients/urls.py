from django.urls import path
from .views import (
    patient_list, patient_detail, patient_add, patient_update, patient_delete
)


app_name = 'patients'

urlpatterns = [
    path('', patient_list),
    path('<int:pk>/', patient_detail),
    path('<int:pk>/update/', patient_update),
    path('<int:pk>/delete/', patient_delete),
    path('add/', patient_add),
]
