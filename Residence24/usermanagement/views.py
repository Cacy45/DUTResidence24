from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
# from .forms import HousingAdminRegistrationForm
from housing.models import HousingAdmin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentLoginForm, AdminLoginForm, RegisterStudentForm, RegisterAdminForm
from usermanagement.models import CustomUser
from django.urls import reverse
from housing.models import HousingAdmin


'''
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on user type
            if user.is_student:
                return redirect('student_dashboard')  # Redirect to student dashboard
            elif user.is_housing_admin:
                return redirect('housing_dashboard')  # Redirect to housing admin dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

'''

# View for student registration

def register_student(request):
    if request.method == 'POST':
        form = RegisterStudentForm(request.POST)
        
        if form.is_valid():
            # Extract the email from the form data
            email = form.cleaned_data.get('email')
            
            # Check if a user with this email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists. Please log in.")
                return redirect('usermanagement:student_login')  # Redirect to login or another appropriate page
            
            # Save the student user to the database
            user = CustomUser.objects.create_user(
                email=email,
                password=form.cleaned_data.get('password'),  # Assuming password is part of your form
                is_student=True  # Set the user as a student
            )
            
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('student:student_dashboard')  # Redirect to the student dashboard
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterStudentForm()

    return render(request, 'usermanagement/register_student.html', {'form': form})
'''
def register_housing_admin(request):
    if request.method == 'POST':
        form = HousingAdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user with the hashed password

            # Create a HousingAdmin instance linked to the user
            housing_admin = HousingAdmin(
                admin_id=user.email,  # Use email as admin_id
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                cell_number=form.cleaned_data['cell_number'],  # Get cell_number from form
                user=user  # Link to the CustomUser
            )
            housing_admin.save()

            login(request, user)  # Log in the user after registration
            return redirect('housing:housing_admin_dashboard')  # Redirect to the admin dashboard
    else:
        form = HousingAdminRegistrationForm()
    
    return render(request, 'authentication/register_housing_admin.html', {'form': form})
'''

def register_admin(request):
    if request.method == 'POST':
        form = RegisterAdminForm(request.POST)
        
        if form.is_valid():
            # Extract the email and password from the form data
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')  # Assuming password is part of your form
            
            # Check if a user with this email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists. Please log in.")
                return redirect('usermanagement:admin_login')  # Redirect to admin login or another appropriate page
            
            # Save the admin user to the database
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                is_housing_admin=True  # Set the user as a housing admin
            )
            
            # Create the HousingAdmin instance
            housing_admin = HousingAdmin(user=user)
            housing_admin.save()
            
            # Log in the user after registration
            login(request, user)  
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('housing:admin_dashboard')  # Redirect to the admin dashboard
        else:
            # Debugging form errors
            print(form.errors)  # Log form errors to the console
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterAdminForm()

    return render(request, 'usermanagement/register_admin.html', {'form': form})





# Student login view
def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful! Welcome back.")
            return redirect('student:student_dashboard')  # Redirect to the student dashboard after login
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = StudentLoginForm()  # Create a blank form for GET requests

    return render(request, 'usermanagement/student_login.html', {'form': form})

# Admin login view
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        
        if form.is_valid():
            # Get the authenticated user from the form
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, "Admin login successful! Welcome.")
                return redirect('housing:admin_dashboard')  # Redirect to the admin dashboard
            else:
                messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AdminLoginForm()  # Create a blank form for GET requests

    return render(request, 'usermanagement/admin_login.html', {'form': form})
'''
# Remeber this original code
# Housing admin login view
def housing_admin_login_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'is_housing_admin') and request.user.is_housing_admin:
        # If the housing admin is already logged in, redirect to the dashboard
        return redirect('housing:housing_admin_dashboard')

    if request.method == 'POST':
        form = HousingAdminLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log in the housing admin
            return redirect('housing:housing_admin_dashboard')  # Redirect to the housing admin dashboard
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = HousingAdminLoginForm()

    return render(request, 'authentication/housing_admin_login_view.html', {'form': form})
'''

'''
# Housing admin login view
def housing_admin_login_view(request):
    if request.method == 'POST':
        form = HousingAdminLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('housing:housing_admin_dashboard')  # Redirect to the housing admin dashboard after login
        else:
            messages.error(request, "Invalid credentials for housing admin.")
    else:
        form = HousingAdminLoginForm()

    return render(request, 'authentication/housing_admin_login_view.html', {'form': form})
'''

# Logout view for both students and housing admins
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect(reverse('main:home.html'))  # Redirect to the homepage after logout

# Student dashboard view (for authenticated student users)
@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('usermanagement:student_login')  # Ensure only students can access this view
    # Render student-specific content
    return render(request, 'student/student_dashboard.html')

# Housing admin dashboard view (for authenticated housing admin users)
@login_required
def admin_dashboard(request):
    if not request.user.is_housing_admin:
        return redirect('usermanagement:admin_login')  # Ensure only housing admins can access this view
    # Render admin-specific content
    return render(request, 'housing/admin_dashboard.html')
