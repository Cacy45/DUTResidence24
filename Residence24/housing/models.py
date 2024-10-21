# housing/models.py
from django.db import models
from usermanagement.models import CustomUser
import uuid
from django.conf import settings  # To reference AUTH_USER_MODEL

class Faculty(models.Model):
    faculty_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    FACULTY_CHOICES = [
        ('Accounting and Informatics', 'Accounting and Informatics'),
        ('Applied Sciences', 'Applied Sciences'),
        ('Management Sciences', 'Management Sciences'),
        ('Engineering and the Built Environment', 'Engineering and the Built Environment'),
        ('Health Sciences', 'Health Sciences'),
        ('Arts & Design', 'Arts & Design'),
    ]

    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, unique=True)
   
    def __str__(self):
        return self.faculty

class HousingAdmin(models.Model):
    # Generate a unique admin_ID
    admin_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Link to User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Admin specific details
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    cell_number = models.CharField(max_length=10)  # Ensure 10-digit format
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} (Admin ID: {self.admin_ID})"


class Residence(models.Model):
    # Generate a unique residence_ID
    residence_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Residence information
    residence_name = models.CharField(max_length=100)
    total_num_of_rooms = models.IntegerField()
    residence_address = models.CharField(max_length=255)
    distance_to_campus = models.DecimalField(max_digits=5, decimal_places=2)  # in kilometers
    # Link to the Faculty model
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.residence_name} (ID: {self.residence_ID})"
    

# housing/models.py (continued)
class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('1-sleeper', '1-sleeper'),
        ('2-sleeper', '2-sleeper'),
    ]
    
    # Room related fields
    room_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    bed_count = models.IntegerField()
    available_beds = models.IntegerField()
    
    # Link each room to a residence
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Room {self.room_ID} in {self.residence.residence_name} ({self.room_type})"
    

