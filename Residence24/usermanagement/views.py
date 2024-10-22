from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

# from .forms import HousingAdminRegistrationForm
from housing.models import HousingAdmin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    StudentLoginForm,
    AdminLoginForm,
    RegisterStudentForm,
    RegisterAdminForm,
)
from usermanagement.models import CustomUser
from django.urls import reverse
from housing.models import HousingAdmin

# View for student registration


def register_student(request):
    if request.method == "POST":
        form = RegisterStudentForm(request.POST)

        if form.is_valid():
            # Extract the email from the form data
            email = form.cleaned_data.get("email")

            # Check if a user with this email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(
                    request, "A user with this email already exists. Please log in."
                )
                return redirect(
                    "usermanagement:student_login"
                )  # Redirect to login or another appropriate page

            # Save the student user to the database
            user = CustomUser.objects.create_user(
                email=email,
                password=form.cleaned_data.get(
                    "password"
                ),  # Assuming password is part of your form
                is_student=True,  # Set the user as a student
            )

            login(request, user)  # Automatically log in the user after registration
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect(
                "student:student_dashboard"
            )  # Redirect to the student dashboard
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = RegisterStudentForm()

    return render(request, "usermanagement/register_student.html", {"form": form})


def register_admin(request):
    if request.method == "POST":
        form = RegisterAdminForm(request.POST)

        if form.is_valid():
            # Extract the email and password from the form data
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get(
                "password"
            )  # Assuming password is part of your form

            # Check if a user with this email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(
                    request, "A user with this email already exists. Please log in."
                )
                return redirect(
                    "usermanagement:admin_login"
                )  # Redirect to admin login or another appropriate page

            # Save the admin user to the database
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                is_housing_admin=True,  # Set the user as a housing admin
            )

            # Create the HousingAdmin instance
            housing_admin = HousingAdmin(user=user)
            housing_admin.save()

            # Log in the user after registration
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect(
                "housing:admin_dashboard"
            )  # Redirect to the admin dashboard
        else:
            # Debugging form errors
            print(form.errors)  # Log form errors to the console
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = RegisterAdminForm()

    return render(request, "usermanagement/register_admin.html", {"form": form})


# Student login view
def student_login(request):
    if request.method == "POST":
        form = StudentLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful! Welcome back.")
                return redirect("student:student_dashboard")
            else:
                messages.error(request, "Invalid email or password. Please try again.")
        else:
            print("Form errors: ", form.errors)
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = StudentLoginForm()  # Create a blank form for GET requests

    return render(request, "usermanagement/student_login.html", {"form": form})


# Admin login view
def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)

        if form.is_valid():
            # Get the authenticated user from the form
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, "Admin login successful! Welcome.")
                return redirect(
                    "housing:admin_dashboard"
                )  # Redirect to the admin dashboard
            else:
                messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AdminLoginForm()  # Create a blank form for GET requests

    return render(request, "usermanagement/admin_login.html", {"form": form})


# Logout view for both students and housing admins
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect(reverse("main:home.html"))  # Redirect to the homepage after logout


# Student dashboard view (for authenticated student users)
@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect(
            "usermanagement:student_login"
        )  # Ensure only students can access this view
    # Render student-specific content
    return render(request, "student/student_dashboard.html")


# Housing admin dashboard view (for authenticated housing admin users)
@login_required
def admin_dashboard(request):
    if not request.user.is_housing_admin:
        return redirect(
            "usermanagement:admin_login"
        )  # Ensure only housing admins can access this view
    # Render admin-specific content
    return render(request, "housing/admin_dashboard.html")
