from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from housing.forms import ResidenceForm, RoomForm, HousingAdminForm
from housing.models import Residence, HousingAdmin, Room, Faculty
from student.models import Student, Application
from django.utils import timezone
from django.contrib import messages
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import random


@login_required
def admin_dashboard(request):
    try:
        admin = HousingAdmin.objects.get(user=request.user)
    except HousingAdmin.DoesNotExist:
        if request.method == "POST":
            form = HousingAdminForm(request.POST)
            if form.is_valid():
                housing_admin = form.save(commit=False)
                housing_admin.user = request.user
                housing_admin.save()
                messages.success(request, "Housing Admin account created successfully.")
                return redirect("housing:admin_dashboard")
        else:
            form = HousingAdminForm()

        return render(request, "housing/create_admin.html", {"form": form})

    # Filter applications by admin's ID
    applications = Application.objects.filter(admin=admin)

    residences = Residence.objects.all()

    context = {
        "admin": admin,
        "residences": residences,
        "applications": applications,
    }
    return render(request, "housing/admin_dashboard.html", context)


@login_required
def manage_residences(request):
    residences = Residence.objects.all()

    if request.method == "POST":
        # Check if the user is trying to edit a residence
        if "edit_residence" in request.POST:
            residence_id = request.POST.get("residence_id")
            residence = get_object_or_404(Residence, id=residence_id)
            form = ResidenceForm(request.POST, instance=residence)
            if form.is_valid():
                form.save()
                messages.success(request, "Residence updated successfully!")
                return redirect("housing:manage_residences")
        elif "delete_residence" in request.POST:
            residence_id = request.POST.get("residence_id")
            residence = get_object_or_404(Residence, id=residence_id)
            residence.delete()
            messages.success(request, "Residence deleted successfully!")
            return redirect("housing:manage_residences")
        else:
            # Adding a new residence
            form = ResidenceForm(request.POST)
            if form.is_valid():
                residence = form.save()  # Save the new residence

                # Generate rooms based on total_num_of_rooms
                for _ in range(residence.total_num_of_rooms):
                    room_type = random.choice(Room.ROOM_TYPE_CHOICES)[
                        0
                    ]  # Choose random room type
                    bed_count = 1 if room_type == "1-sleeper" else 2
                    available_beds = bed_count  # Initially, all beds are available

                    Room.objects.create(
                        room_type=room_type,
                        bed_count=bed_count,
                        available_beds=available_beds,
                        residence=residence,
                    )

                messages.success(request, "Residence and rooms added successfully!")
                return redirect("housing:manage_residences")
    else:
        form = ResidenceForm()

    return render(
        request,
        "housing/manage_residences.html",
        {
            "form": form,
            "residences": residences,
        },
    )


@login_required
def add_room(request, residence_id):
    try:
        residence = Residence.objects.get(
            residence_ID=residence_id
        )  # Ensure you're using residence_ID here
    except Residence.DoesNotExist:
        messages.error(request, "The requested residence does not exist.")
        return redirect("housing:manage_residences")

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.residence = residence  # Link room to the residence
            room.save()
            messages.success(request, "Room added successfully!")
            return redirect("housing:manage_residences")

    form = RoomForm()
    return render(
        request, "housing/add_room.html", {"form": form, "residence": residence}
    )


def add_rooms_bulk(request, residence_id):
    residence = Residence.objects.get(residence_ID=residence_id)

    if request.method == "POST":
        room_data = request.POST.getlist(
            "rooms"
        )  # Assuming you're getting room data from a form
        for data in room_data:
            room_type, bed_count, available_beds = data.split(",")
            Room.objects.create(
                room_type=room_type,
                bed_count=bed_count,
                available_beds=available_beds,
                residence=residence,
            )
        messages.success(request, "Rooms added successfully!")
        return redirect("housing:manage_residences")

    return render(request, "housing/add_rooms_bulk.html", {"residence": residence})


# View for managing applications
@login_required
def manage_applications(request):
    # take this filter one out
    applications = Application.objects.select_related("student").filter(
        student__isnull=False
    )

    if request.method == "POST":
        print(request.POST)  # Debugging to check the posted data
        application_id = request.POST.get("application_id")
        application = get_object_or_404(Application, application_ID=application_id)
        print("Application ID:", application_id)
        print(request.user.__dict__)

        # Get the HousingAdmin instance for the logged-in user !!!! dont remove this
        admin_instance = get_object_or_404(
            HousingAdmin, user_id=request.user.id
        )  # Adjust based on your setup

        if "approve" in request.POST:
            application.status = "Approved"
            application.admin = admin_instance  # Assign HousingAdmin instance
            application.save()
            return redirect("housing:manage_applications")

        elif "reject" in request.POST:
            application.status = "Rejected"
            application.admin = admin_instance  # Assign HousingAdmin instance
            application.save()
            return redirect("housing:manage_applications")

    return render(
        request,
        "housing/manage_applications.html",
        {
            "applications": applications,
        },
    )


@login_required
def assign_room(request, student_id):
    # Attempt to retrieve the student; if not found, redirect with an error message
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        messages.error(request, "The requested student does not exist.")
        return redirect("housing:admin_dashboard")  # Redirect to the admin dashboard

    # Get the student's preferred room type from the application
    preferred_room_type = (
        student.preferred_room_type
    )  # Adjust based on your model structure

    # Filter rooms based on preferred room type and available beds
    rooms = Room.objects.filter(room_type=preferred_room_type, available_beds__gt=0)

    if request.method == "POST":
        room_id = request.POST.get("room")  # Using .get() for safer access

        # Attempt to retrieve the room; if not found, handle the situation
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            messages.error(request, "The selected room does not exist.")
            return redirect(
                "housing:admin_dashboard"
            )  # Redirect to the admin dashboard

        # Check if there is space in the room
        if room.available_beds > 0:
            # Count current students assigned to this room
            current_assignments = Room.objects.filter(id=room.id).count()

            # Check if assigning this student exceeds the bed count
            if current_assignments < room.bed_count:
                # Create a room assignment instance
                Room.objects.create(
                    room=room,
                    student=student,
                    residence=room.residence,
                    assignment_date=datetime.date.today(),
                    status="Assigned",
                )

                # Update available beds
                room.available_beds -= 1  # Reduce by one since we're adding one student
                room.save()

                # Update the residence's available rooms (if needed)
                residence = room.residence
                residence.available_rooms -= 1  # Decrease the count of available rooms
                residence.save()

                messages.success(
                    request, f"Room assigned to {student.first_name} successfully."
                )
            else:
                messages.error(request, "The selected room is fully occupied.")
        else:
            messages.error(request, "The selected room is no longer available.")

        return redirect("housing:admin_dashboard")

    return render(
        request, "housing/assign_room.html", {"student": student, "rooms": rooms}
    )
