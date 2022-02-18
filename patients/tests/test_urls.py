from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.urls.exceptions import NoReverseMatch

import patients.views


PATIENT_VIEWS = (
    patients.views.HomePageView,
    patients.views.PatientListView,
    patients.views.PatientDetailView,
    patients.views.PatientAddView,
    patients.views.PatientUpdateView,
    patients.views.PatientDeleteView,
    patients.views.AppointmentStatusListView,
    patients.views.AppointmentStatusDetailView,
    patients.views.PatientAppointmentStatusUpdateView,
)


PATIENT_URL_NAMES = (
    'home-page',
    'patients:patient-list',
    'patients:patient-detail',
    'patients:patient-add',
    'patients:patient-update',
    'patients:patient-delete',
    'patients:appointment-stats',
    'patients:appointment-stat-detail',
    'patients:patient-appointment-status-update',
)


class TestUrls(SimpleTestCase):

    def test_patient_urls_resolve_to_correct_view(self):
        for name, view in zip(PATIENT_URL_NAMES, PATIENT_VIEWS):
            try:
                url = reverse(name)
            except NoReverseMatch:
                url = reverse(name, args=['1'])
            self.assertEquals(resolve(url).func.view_class, view)
