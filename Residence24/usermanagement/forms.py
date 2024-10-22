from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser
from housing.models import HousingAdmin
from student.models import Student
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class RegisterStudentForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Create a password", "required": "required"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm your password", "required": "required"}
        )
    )

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True  # Mark this user as a student
        if commit:
            user.set_password(self.cleaned_data["password1"])  # Set password correctly
            user.save()
        return user

    # Include your validation methods here...


"""
# Form for student registration
class RegisterStudentForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True   # Mark this user as a student
        if commit:
            user.save()
        return user
"""


class RegisterAdminForm(UserCreationForm):
    cell_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your cell number", "required": "required"}
        ),
        help_text="Cell number must be 10 digits.",
    )

    class Meta:
        model = CustomUser  # Using CustomUser for user creation
        fields = [
            "email",
            "first_name",
            "last_name",
            "cell_number",
            "password1",
            "password2",
        ]
        widgets = {
            "email": forms.EmailInput(
                attrs={"placeholder": "Enter your email", "required": "required"}
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": "Enter your first name", "required": "required"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Enter your last name", "required": "required"}
            ),
            "password1": forms.PasswordInput(
                attrs={"placeholder": "Create a password", "required": "required"}
            ),
            "password2": forms.PasswordInput(
                attrs={"placeholder": "Confirm your password", "required": "required"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_housing_admin = True  # Mark this user as a housing admin
        if commit:
            user.save()  # Save the user instance first

            # Now create the corresponding HousingAdmin object
            HousingAdmin.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                cell_number=self.cleaned_data[
                    "cell_number"
                ],  # Use cleaned data for cell number
            )
        return user

    def clean_cell_number(self):
        cell_number = self.cleaned_data.get("cell_number")
        if len(cell_number) != 10 or not cell_number.isdigit():
            raise forms.ValidationError("Cell number must be 10 digits.")
        return cell_number

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not password1:
            self.add_error("password1", "This field is required.")
        if not password2:
            self.add_error("password2", "This field is required.")
        elif password1 != password2:
            self.add_error("password2", "Passwords do not match.")

        return cleaned_data


"""
class HousingAdminRegistrationForm(UserCreationForm):
    cell_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your cell number', 'required': 'required'}),
        help_text="Cell number must be 12 digits."
    )

    class Meta:
        model = CustomUser  # Using CustomUser for user creation
        fields = ['email', 'first_name', 'last_name', 'cell_number', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'required': 'required'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'required': 'required'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Create a password', 'required': 'required'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'required': 'required'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_housing_admin = True  # Mark this user as a housing admin
        if commit:
            user.save()
        return user

    def clean_cell_number(self):
        cell_number = self.cleaned_data.get('cell_number')
        if len(cell_number) != 12 or not cell_number.isdigit():
            raise forms.ValidationError("Cell number must be 12 digits.")
        return cell_number

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data
"""


"""'
# Form for housing admin registration
class HousingAdminSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_housing_admin = True  # Mark this user as a housing admin
        if commit:
            user.save()
        return user
"""


class StudentLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your DUT email", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password", "class": "form-control"}
        )
    )

    # def clean(self):
    #     cleaned_data = super().clean()
    #     # email = cleaned_data.get("email")
    #     # password = cleaned_data.get("password")

    #     # if email and password:
    #     #     # Authenticate the student user
    #     #     user = authenticate(username=email, password=password)

    #     #     if user is None or not user.is_student:
    #     #         raise forms.ValidationError("Invalid email or password for a student.")

    #     #     elif not user.is_active:
    #     #         raise forms.ValidationError("This account is inactive.")

    #     return cleaned_data

    # def get_user(self):
    #     """Retrieve the authenticated user after successful validation"""
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     user = authenticate(username=email, password=password)
        
    #     print(user)
        
    #     return user


class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password", "class": "form-control"}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            # Authenticate the housing admin user using email and password
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
            elif not hasattr(user, "is_housing_admin") or not user.is_housing_admin:
                raise forms.ValidationError(
                    "This account is not a housing admin account."
                )
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")

        return cleaned_data

    def get_user(self):
        """Retrieve the authenticated user after successful validation"""
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        return user


'''
class HousingAdminLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Authenticate the housing admin user
            user = authenticate(username=email, password=password)  # Use email as the username
            if user is None or not hasattr(user, 'is_housing_admin') or not user.is_housing_admin:
                raise forms.ValidationError("Invalid email or password for a housing admin.")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")
        
        return cleaned_data

    def get_user(self):
        """ Retrieve the authenticated user after successful validation """
        email = self.cleaned_data.get('email')
        return CustomUser.objects.get(email=email)  # Adjust this if necessary
'''
