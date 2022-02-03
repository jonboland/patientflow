from django.urls import path
from .views import (
    StaffListView, staff_member_add, StaffMemberDetailView, 
    staff_member_update, StaffMemberDeleteView,   
)


app_name = 'staff'
 
urlpatterns = [
    path('', StaffListView.as_view(), name='staff-list'),
    path('<int:pk>/', StaffMemberDetailView.as_view(), name='staff-member-detail'),
    path('<int:pk>/update/', staff_member_update, name='staff-member-update'),
    path('<int:pk>/delete/', StaffMemberDeleteView.as_view(), name='staff-member-delete'),
    path('add/', staff_member_add, name='staff-member-add'),
]
