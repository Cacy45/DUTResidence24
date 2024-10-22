# student/models.py
from django.db import models
from django.conf import settings  # To reference AUTH_USER_MODEL

import uuid

from housing.models import Residence, Faculty, HousingAdmin
from usermanagement.models import CustomUser


class Student(models.Model):
    # Linking Student model to the User model using OneToOneField
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Fields related to student information
    student_ID = models.CharField(max_length=8, unique=True)  # Extracted from email
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    GENDER_CHOICES = [
        ("Female", "Female"),
        ("Male", "Male"),
        ("Other", "Other"),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    home_address_street = models.CharField(max_length=255)
    home_address_suburb = models.CharField(max_length=100)
    home_address_city = models.CharField(max_length=100)
    home_address_postal_code = models.CharField(max_length=4)

    is_local = models.BooleanField()  # Boolean to check if the student is local

    LEVEL_OF_STUDY_CHOICES = [
        ("1st year", "1st year"),
        ("2nd year", "2nd year"),
        ("3rd year", "3rd year"),
        ("4th year", "4th year"),
        ("Postgraduate", "Postgraduate"),
    ]
    level_of_study = models.CharField(max_length=20, choices=LEVEL_OF_STUDY_CHOICES)

    # Link to the Faculty model
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    ROOM_TYPE_CHOICES = [
        ("1-sleeper", "1-sleeper"),
        ("2-sleeper", "2-sleeper"),
    ]
    preferred_room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_ID})"

    def save(self, *args, **kwargs):
        try:
            # Check if the postal code starts with "400"
            if self.home_address_postal_code.startswith("400"):
                self.is_local = True

            else:
                self.is_local = False

        except Exception as e:
            # Log the error or handle it accordingly
            print(f"Error determining location: {e}")
            self.is_local = False  # Default to False if there's an error

        super(Student, self).save(*args, **kwargs)


class Application(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    # Generate a unique application_ID
    application_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Status of the application
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    application_date = models.DateTimeField(auto_now_add=True)

    # Link to Student and Residence models
    student = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True, blank=True
    )
    residence = models.ForeignKey(
        Residence, on_delete=models.SET_NULL, null=True, blank=True
    )
    admin = models.ForeignKey(
        HousingAdmin, null=True, blank=True, on_delete=models.SET_NULL
    )  # Link to HousingAdmin

    def __str__(self):
        # Handle cases where student or residence might be None
        student_info = (
            f"{self.student.first_name} {self.student.last_name}"
            if self.student
            else "No Student"
        )
        residence_info = self.residence.residence_name if self.residence else "No Residence"

        return f"Application {self.application_ID} ({student_info}) - Residence: {residence_info}"
