# housing/urls.py
from django.urls import path
from . import views

app_name = 'housing'  # This is the namespace for the housing app

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Ensure this view exists
    # path('residence/<uuid:residence_id>/', views.manage_residences, name='manage_residences'),
    path('manage-residences/', views.manage_residences, name='manage_residences'),
    # path('add_room/<uuid:residence_id>/', views.add_room, name='add_room'),
    path('add-room/', views.add_room, name='add_room'),
    # path('residence/new', views.create_or_update_residence, name='create_or_update_residence'),
    # path('application/<uuid:application_id>/', views.manage_applications, name='manage_application'),
    path('manage-applications/', views.manage_applications, name='manage_applications'),
    # path('assign-room/<uuid:student_id>/', views.assign_room, name='assign_room'),
    path('assign-room/', views.assign_room, name='assign_room'),
    # path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Ensure this view exists
   
]
