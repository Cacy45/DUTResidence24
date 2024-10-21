# usermanagement/urls.py
from django.urls import path
from . import views

app_name = "usermanagement"

urlpatterns = [
    path("housing/register/", views.register_admin, name="register_admin"),
    path("housing/login/", views.admin_login, name="admin_login"),
    path("student/login/", views.student_login, name="student_login"),
    path("student/register/", views.register_student, name="register_student"),
    path("logout/", views.logout_view, name="logout"),
    # path('registration-success/', views.registration_success, name='success_url'),  # Success URL
]
