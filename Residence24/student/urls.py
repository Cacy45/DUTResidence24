# student/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "student"  # This is the namespace for the student app

urlpatterns = [
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path(
        "student/application-status/",
        views.application_status,
        name="application_status",
    ),
    path("student/select-residence/", views.select_residence, name="select_residence"),
    path("student/submit-residence-choice/", views.submit_residence_choice, name="submit_residence_choice"),
    path(
        "student/residence-details/", views.residence_details, name="residence_details"
    ),
    path(
        "student/residence-application/",
        views.residence_application,
        name="residence_application",
    ),
    path(
        "student/logout/",
        auth_views.LogoutView.as_view(
            next_page="/", http_method_names=["get", "post", "options"]
        ),
        name="logout",
    ),
]
