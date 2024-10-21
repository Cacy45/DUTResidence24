# student/urls.py
from django.urls import path
from . import views

app_name = "student"  # This is the namespace for the student app

urlpatterns = [
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    # path(
    #     "student/residence-application/",
    #     views.residence_application,
    #     name="residence_application",
    # ),
    path(
        "student/application-status/",
        views.application_status,
        name="application_status",
    ),
    path("student/select-residence/", views.select_residence, name="select_residence"),
    path(
        "student/residence-details/", views.residence_details, name="residence_details"
    ),
    path("student/residence-application/", views.residence_application, name="residence_application"),
]
