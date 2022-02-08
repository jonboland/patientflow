from django.urls import path
from .views import (
    PatientListView,
    PatientDetailView,
    PatientAddView,
    PatientUpdateView,
    PatientDeleteView,
    PatientAssignView,
    AppointmentStatusListView,
)


app_name = 'patients'

urlpatterns = [
    path('', PatientListView.as_view(), name='patient-list'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('<int:pk>/update/', PatientUpdateView.as_view(), name='patient-update'),
    path('<int:pk>/delete/', PatientDeleteView.as_view(), name='patient-delete'),
    path('add/', PatientAddView.as_view(), name='patient-add'),
    path('<int:pk>/assign/', PatientAssignView.as_view(), name='patient-assign'),
    path(
        'appointment-stats/',
        AppointmentStatusListView.as_view(),
        name='appointment-stats',
    ),
]
