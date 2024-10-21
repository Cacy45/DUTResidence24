from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from student.forms import ResidenceApplicationForm, CreateProfileForm
from django.contrib import messages
from student.models import Application, Student  # Your model for student applications
from housing.models import Residence, Faculty
from usermanagement.models import CustomUser


@login_required
def student_dashboard(request):

    if not request.user.is_student:
        return HttpResponseForbidden("You are not authorized to access this page.")
    # Student-specific dashboard logic here
    return render(request, "student/student_dashboard.html", {"user": request.user})


@login_required
def residence_application(request):
    # Attempt to get the logged-in user's associated Student instance
    try:
        student = Student.objects.get(student_ID=request.user.student_id)

        # Check if the student's profile is complete (i.e., mandatory fields are filled)
        if not (
            student.first_name and student.last_name and student.home_address_street
        ):
            messages.warning(
                request, "Please complete your profile before applying for residence."
            )
            return redirect(
                "student:create_profile"
            )  # Redirect them to fill in profile details
    except Student.DoesNotExist:
        messages.error(
            request,
            "Student record not found. Please ensure your account is set up correctly.",
        )
        return redirect(
            "student:create_profile"
        )  # If no student record, redirect to create profile

    if request.method == "POST":
        form = ResidenceApplicationForm(request.POST)

        if form.is_valid():
            student_application = form.save(commit=False)
            student_application.student = student  # Link the student to the application
            student_application.home_address_street = student.home_address_street
            student_application.faculty = form.cleaned_data[
                "faculty"
            ]  # Optionally allow updating the faculty field
            student_application.save()
            messages.success(
                request, "Your application has been submitted successfully."
            )
            return redirect("student:student_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        # Pre-populate form fields with the student's profile information
        form = ResidenceApplicationForm(
            initial={
                "home_address_street": student.home_address_street,
                "home_address_suburb": student.home_address_suburb,
                "home_address_city": student.home_address_city,
                "home_address_postal_code": student.home_address_postal_code,
                "faculty": student.faculty,
                # Add any other fields you want to pre-populate
            }
        )

    return render(
        request,
        "student/residence_application.html",
        {
            "form": form,
            "user": request.user,
            "student": student,  # Pass student object to the template
        },
    )


@login_required
def create_profile(request):
    try:
        student = Student.objects.get(student_ID=request.user.student_id)
    except Student.DoesNotExist:
        student = None

    if request.method == "POST":
        form = CreateProfileForm(request.POST, instance=student)

        if form.is_valid():
            student = form.save(commit=False)
            student.student_ID = (
                request.user.student_id
            )  # Ensure the correct student ID is linked
            student.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("student:student_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CreateProfileForm(instance=student)
        # Prepopulate the student_ID
        form.fields["student_ID"].initial = request.user.student_id
        """
        ============================
        Dummy data
        ============================
        """
        _faculty = Faculty.objects.get(faculty_ID="c04a24b179554e94a33819ff9fab4618")

        dummy_student = Student(
            faculty=_faculty,
            first_name="John",
            last_name="Doe",
            gender="Male",
            home_address_city="Durban",
            home_address_street="70 Steve Biko Road",
            home_address_suburb="Musgrave",
            home_address_postal_code="4001",
            # is_local=True,
            level_of_study="Undergraduate",
            preferred_room_type="1-sleeper",
        )
        print(dummy_student.__dict__)
        form.fields = dummy_student.__dict__

    return render(request, "student/create_profile.html", {"form": form})


"""
@login_required
def submit_residence_application(request):
    # Get the currently logged-in student
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = ResidenceApplicationForm(request.POST)  # Assuming you have a form for applications

        if form.is_valid():
            # Create a new application instance but do not save yet
            application = form.save(commit=False)
            application.student_ID = student  # Link the application to the logged-in student
            
            # Set the initial status to 'Pending'
            application.status = 'Pending'
            application.save()

            messages.success(request, 'Your residence application has been submitted successfully.')
            return redirect('housing:application_status')  # Redirect to application status page

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = ResidenceApplicationForm()  # If GET request, create an empty form

    return render(request, 'housing/residence_application.html', {
        'form': form,
        'student': student  # Pass the student object if needed
    })
"""


@login_required
def select_residence(request):
    try:
        # Fetch the Student instance associated with the current user
        student = Student.objects.get(user=request.user)

        # Get the application status for the current student
        application = Application.objects.get(student=student)
        application_status = (
            application.status
        )  # Assuming 'status' is a field in Application model

        # Handle different application statuses
        if application_status == "Declined":
            return render(
                request,
                "student/select_residence.html",
                {"application_status": application_status},
            )

        elif application_status == "Approved":
            # Filter residences based on the student's faculty or other criteria
            residences = Residence.objects.filter(
                faculty=student.faculty
            )  # Assuming faculty is a field in Residence and Student
            return render(
                request,
                "student/select_residence.html",
                {"application_status": application_status, "residences": residences},
            )

        # If status is not approved or declined, consider it as "Pending"
        return render(
            request, "student/select_residence.html", {"application_status": "Pending"}
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

        # Save the choice in the database (implement as needed)
        # For example, you might have a model to save this choice
        student_application = Application.objects.get(student=request.user)
        student_application.residence_ID = residence_id
        student_application.student_ID.preferred_room_type = room_type
        student_application.save()

        messages.success(request, "Your residence choice has been saved successfully.")
        return redirect(
            "student_dashboard"
        )  # Redirect to the dashboard or appropriate page

    return redirect("select_residence")  # Redirect back if not a POST request


def application_status(request):
    applications = Application.objects.filter(
        student__student_ID=request.user.student_id
    )
    # application = Application.objects.get(student_ID=request.user.student)
    return render(
        request, "student/application_status.html", {"application": applications}
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


"""
# View for students to apply for residence
@login_required
def apply_for_residence(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user.student  # assuming user has a student profile
            application.application_date = timezone.now()
            application.status = 'Pending'  # default status
            application.save()
            messages.success(request, 'Application submitted successfully.')
            return redirect('student:student_dashboard')  # Redirect to the student dashboard after successful submission
    else:
        form = ApplicationForm()

    return render(request, 'housing/apply_for_residence.html', {'form': form})
"""
