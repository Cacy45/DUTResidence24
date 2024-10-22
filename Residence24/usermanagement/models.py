from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """Custom user manager for CustomUser model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Set the password
        user.save(using=self._db)  # Save user to the database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Ensure a superuser always has these attributes
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model that uses email as the username field."""

    username = None  # Remove username field
    email = models.EmailField(
        unique=True
    )  # Email will be the unique identifier for login
    is_student = models.BooleanField(default=False)
    is_housing_admin = models.BooleanField(default=False)
    student_id = models.CharField(
        max_length=8, blank=True, null=True, unique=True
    )  # Unique student ID

    USERNAME_FIELD = "email"  # Use email for authentication
    REQUIRED_FIELDS = []  # No additional required fields for user creation

    objects = CustomUserManager()  # Set the custom user manager

    def clean(self):
        """Custom validation for student and housing admin emails."""
        super().clean()  # Ensure the parent clean method is called

        if self.is_student:
            if not self.email.endswith("@dut4life.ac.za"):
                raise ValidationError("Student email must end with '@dut4life.ac.za'")
            # Extract student ID from the email
            student_id = self.email.split("@")[0]
            if not student_id.isdigit() or len(student_id) != 8:
                raise ValidationError("Invalid student ID in email")
            self.student_id = student_id

        if self.is_housing_admin and not self.email.endswith("@dut4life.ac.za"):
            raise ValidationError("Housing admin must use a valid DUT email")

    def save(self, *args, **kwargs):
        """Override save to ensure validation happens before saving."""
        self.full_clean()  # Run validations before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
