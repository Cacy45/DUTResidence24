from django.contrib.auth.models import AbstractUser, BaseUserManager  # Added BaseUserManager import
from django.db import models
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):  # New custom user manager class
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):  # New method for creating superuser
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Call the create_user method to handle the user creation
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # We don't need the username field
    email = models.EmailField(unique=True)  # Email will be the unique identifier for login
    is_student = models.BooleanField(default=False)
    is_housing_admin = models.BooleanField(default=False)
    student_id = models.CharField(max_length=8, blank=True, null=True, unique=True)  # Ensure student ID is unique

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = []  # No other required fields apart from email

    objects = CustomUserManager()  # Set the custom user manager  # New line

    def clean(self):
        """Custom validation for student and housing admin emails."""
        if self.is_student and self.email.endswith('@dut4life.ac.za'):
            # Extract student ID from the email (before '@')
            student_id = self.email.split('@')[0]
            if not student_id.isdigit() or len(student_id) != 8:
                raise ValidationError("Invalid student ID in email")
            self.student_id = student_id
        
        # Ensure housing admins use the correct email domain, if required
        if self.is_housing_admin and not self.email.endswith('@dut4life.ac.za'):
            raise ValidationError("Housing admin must use a valid DUT email")

        super().clean()  # Call parent class's clean() to maintain other validations

    def save(self, *args, **kwargs):
        """Override save to ensure validation happens before saving."""
        self.full_clean()  # Run validations before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
