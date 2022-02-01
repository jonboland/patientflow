from django.urls import path
from .views import (
    StaffListView, StaffMemberAddView, StaffMemberDetailView, StaffMemberUpdateView, StaffMemberDeleteView
)


app_name = 'staff'
 
urlpatterns = [
    path('', StaffListView.as_view(), name='staff-list'),
    path('<int:pk>/', StaffMemberDetailView.as_view(), name='staff-member-detail'),
    path('<int:pk>/update/', StaffMemberUpdateView.as_view(), name='staff-member-update'),
    path('<int:pk>/delete/', StaffMemberDeleteView.as_view(), name='staff-member-delete'),
    path('add/', StaffMemberAddView.as_view(), name='staff-member-add'),
]
