from django import forms
from .models import Application, Student  # Import Application model
from housing.models import Faculty

"""
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
        residence_info = self.residence.name if self.residence else "No Residence"

        return f"Application {self.application_ID} ({student_info}) - Residence: {residence_info}"

"""


class ResidenceApplicationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "home_address_street",
            "home_address_suburb",
            "home_address_city",
            "home_address_postal_code",
            "gender",
            "faculty",
            "preferred_room_type",
            "level_of_study",
        ]

    def __init__(self, *args, **kwargs):
        super(ResidenceApplicationForm, self).__init__(*args, **kwargs)

        # Adding placeholders and other attributes
        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "Enter your first name", "class": "form-control"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Enter your last name", "class": "form-control"}
        )
        self.fields["home_address_street"].widget.attrs.update(
            {"placeholder": "Street name", "class": "form-control"}
        )
        self.fields["home_address_suburb"].widget.attrs.update(
            {"placeholder": "Suburb", "class": "form-control"}
        )
        self.fields["home_address_city"].widget.attrs.update(
            {"placeholder": "City", "class": "form-control"}
        )
        self.fields["home_address_postal_code"].widget.attrs.update(
            {"placeholder": "Postal code", "class": "form-control"}
        )
        self.fields["faculty"].widget.attrs.update({"class": "form-control"})
        self.fields["gender"].widget.attrs.update({"class": "form-control"})
        self.fields["preferred_room_type"].widget.attrs.update(
            {"class": "form-control"}
        )
        self.fields["level_of_study"].widget.attrs.update({"class": "form-control"})
