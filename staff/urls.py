from django.urls import path
from .views import StaffListView, StaffMemberAddView


app_name = 'staff'
 
urlpatterns = [
    path('', StaffListView.as_view(), name='staff-list'),
    path('add/', StaffMemberAddView.as_view(), name='staff-member-add'),
]
