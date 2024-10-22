from django.http import HttpResponseForbidden
from student.forms import ResidenceApplicationForm
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from datetime import datetime

from student.models import Application, Student  # Your model for student applications
from housing.models import Residence, Faculty

# from usermanagement.models import CustomUser


@login_required
def student_dashboard(request):
    # Attempt to get the logged-in user's associated Student instance
    application = None

    try:
        student = Student.objects.get(student_ID=request.user.student_id)
        application = Application.objects.get(student_id=student.id)

        print("Application found for user: ", request.user.student_id)

    except (Student.DoesNotExist, Application.DoesNotExist):
        messages.info(request, "Please make an application for residence.")
        print("No application found for user: ", request.user.student_id)

    if not request.user.is_student:
        return HttpResponseForbidden("You are not authorized to access this page.")

    # Student-specific dashboard logic here
    return render(
        request,
        "student/student_dashboard.html",
        {"user": request.user, "application": application},
    )


@login_required
def residence_application(request):
    try:
        student = Student.objects.get(student_ID=request.user.student_id)
    except Student.DoesNotExist:
        student = None

    if request.method == "POST":
        form = ResidenceApplicationForm(request.POST, instance=student)

        if form.is_valid():
            # Retrieve student details
            student = form.save(commit=False)

            student.student_ID = request.user.student_id
            student.user_id = request.user.id
            student.save()

            messages.success(request, "Application submitted successfully.")

            # Create Application or Update if it exists
            try:
                application = Application.objects.get(student_id=student.id)

            except Application.DoesNotExist:
                application = Application()
                application.application_date = datetime.now()
                application.student_id = student.id

            application.save()

            return redirect("student:student_dashboard")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = ResidenceApplicationForm(instance=student)

    return render(request, "student/residence_application.html", {"form": form})


@login_required
def submit_residence_application(request):
    # Get the currently logged-in student
    student = get_object_or_404(Student, user=request.user)

    if request.method == "POST":
        form = ResidenceApplicationForm(
            request.POST
        )  # Assuming you have a form for applications

        if form.is_valid():
            # Create a new application instance but do not save yet
            application = form.save(commit=False)
            application.student_ID = (
                student  # Link the application to the logged-in student
            )

            # Set the initial status to 'Pending'
            application.status = "Pending"
            application.save()

            messages.success(
                request, "Your residence application has been submitted successfully."
            )
            return redirect(
                "housing:application_status"
            )  # Redirect to application status page

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = ResidenceApplicationForm()  # If GET request, create an empty form

    return render(
        request,
        "housing/residence_application.html",
        {"form": form, "student": student},  # Pass the student object if needed
    )


@login_required
def select_residence(request):
    try:
        # Fetch the Student instance associated with the current user
        student = Student.objects.get(user=request.user)

        # Get the application status for the current student
        application = Application.objects.get(student=student)

        # Handle different application statuses
        if application.status == "Declined":
            return render(
                request,
                "student/select_residence.html",
                {"application": application},
            )

        elif application.status == "Approved":
            # Filter residences based on the student's faculty or other criteria
            residences = Residence.objects.filter(
                faculty=student.faculty
            )  # Assuming faculty is a field in Residence and Student

            for residence in residences:
                residence.image_path = (
                    residence.residence_name.lower().replace(" ", "_") + ".jpg"
                )

            return render(
                request,
                "student/select_residence.html",
                {"application": application, "residences": residences},
            )

        # If status is not approved or declined, consider it as "Pending"
        return render(
            request,
            "student/select_residence.html",
            {"application": application},
        )

    except Student.DoesNotExist:
        # Handle the case where the student record does not exist
        return render(
            request,
            "student/select_residence.html",
            {"error": "Student record not found."},
        )

    except Application.DoesNotExist:
        # Handle the case where the application record does not exist
        return render(
            request,
            "student/select_residence.html",
            {"error": "Application record not found."},
        )


@login_required
def submit_residence_choice(request):
    if request.method == "POST":
        residence_id = request.POST.get("residence")
        room_type = request.POST.get("room_type")

        student = Student.objects.get(user=request.user)
        student_application = Application.objects.get(student=student)

        print(student_application)
        student_application.residence_id = residence_id
        student_application.save()

        messages.success(request, "Your residence choice has been saved successfully.")
        return redirect(
            "student:student_dashboard"
        )  # Redirect to the dashboard or appropriate page

    return redirect("select_residence")  # Redirect back if not a POST request


def application_status(request):
    application = None

    try:
        student = Student.objects.get(student_ID=request.user.student_id)
        application = Application.objects.get(student_id=student.id)

    except (Student.DoesNotExist, Application.DoesNotExist):
        return redirect("student:student_dashboard")

    return render(
        request, "student/application_status.html", {"application": application}
    )


def residence_details(request):
    try:
        # Get the residence associated with the logged-in student's application
        residence_application = Application.objects.get(student=request.user.student)
        residence = (
            residence_application.residence
        )  # Access the related residence through the application
    except Application.DoesNotExist:
        residence = None

    return render(request, "student/residence_details.html", {"residence": residence})
