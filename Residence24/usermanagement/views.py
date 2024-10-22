from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
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


# View for student registration
def register_student(request):
    if request.method == "POST":
        form = RegisterStudentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if CustomUser.objects.filter(email=email).exists():
                messages.error(
                    request, "A user with this email already exists. Please log in."
                )
                return redirect("usermanagement:student_login")
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect("student:student_dashboard")
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = RegisterStudentForm()
    return render(request, "usermanagement/register_student.html", {"form": form})


# View for admin registration
def register_admin(request):
    if request.method == "POST":
        form = RegisterAdminForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if CustomUser.objects.filter(email=email).exists():
                messages.error(
                    request, "A user with this email already exists. Please log in."
                )
                return redirect("usermanagement:admin_login")
            user = form.save()
            HousingAdmin.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect("housing:admin_dashboard")
        else:
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
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, "Login successful! Welcome back.")
                return redirect("student:student_dashboard")
            else:
                messages.error(request, "Invalid email or password. Please try again.")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = StudentLoginForm()
    return render(request, "usermanagement/student_login.html", {"form": form})


# Admin login view
def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, "Admin login successful! Welcome.")
                return redirect("housing:admin_dashboard")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AdminLoginForm()
    return render(request, "usermanagement/admin_login.html", {"form": form})


# Logout view for both students and housing admins
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect(reverse("main:home.html"))


# Student dashboard view (for authenticated student users)
@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect("usermanagement:student_login")
    return render(request, "student/student_dashboard.html")


# Housing admin dashboard view (for authenticated housing admin users)
@login_required
def admin_dashboard(request):
    if not request.user.is_housing_admin:
        return redirect("usermanagement:admin_login")
    return render(request, "housing/admin_dashboard.html")
