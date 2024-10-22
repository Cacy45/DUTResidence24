from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from usermanagement.models import CustomUser
from housing.models import HousingAdmin

from .forms import (
    RegisterStudentForm,
    RegisterAdminForm,
    StudentLoginForm,
    AdminLoginForm,
)

user_email = "22341556@dut4life.ac.za"


class CustomUserTestCase(TestCase):
    def setUp(self):
        # Create a new user
        self.user = CustomUser.objects.create_user(
            email=user_email, password="your_plaintext_password"
        )
        self.user.is_student = True  # Or any other fields you want to set
        self.user.save()

    def tearDown(self):
        CustomUser.objects.get(email=user_email).delete()
        return super().tearDown()

    def test_password_check(self):
        # Retrieve the user
        user = CustomUser.objects.get(email=user_email)

        # Check the password
        self.assertTrue(
            user.check_password("your_plaintext_password"), "Password is correct!"
        )
        self.assertFalse(
            user.check_password("wrong_password"), "Password is incorrect!"
        )

    def test_authentication(self):
        # Authenticate the user
        user = authenticate(email=user_email, password="your_plaintext_password")
        self.assertIsNotNone(user, "User is authenticated!")
        self.assertEqual(user.email, user_email, "User email is correct!")


User = get_user_model()


class RegisterStudentFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "email": "22341556@dut4life.ac.za",
            "password1": "strong_password_123",
            "password2": "strong_password_123",
        }
        form = RegisterStudentForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.is_student)
        self.assertTrue(user.check_password("strong_password_123"))

    def test_password_mismatch(self):
        form_data = {
            "email": "22341556@dut4life.ac.za",
            "password1": "strong_password_123",
            "password2": "different_password_123",
        }
        form = RegisterStudentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Passwords do not match.", form.errors["password2"])


class RegisterAdminFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "email": "admin@dut4life.ac.za",
            "first_name": "Admin",
            "last_name": "User",
            "cell_number": "0123456789",
            "password1": "strong_password_123",
            "password2": "strong_password_123",
        }
        form = RegisterAdminForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.is_housing_admin)
        self.assertTrue(user.check_password("strong_password_123"))
        self.assertTrue(HousingAdmin.objects.filter(user=user).exists())

    def test_invalid_cell_number(self):
        form_data = {
            "email": "admin@dut4life.ac.za",
            "first_name": "Admin",
            "last_name": "User",
            "cell_number": "12345",
            "password1": "strong_password_123",
            "password2": "strong_password_123",
        }
        form = RegisterAdminForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Cell number must be 10 digits.", form.errors["cell_number"])


class StudentLoginFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="22341556@dut4life.ac.za",
            password="strong_password_123",
            is_student=True,
        )

    def test_valid_login(self):
        form_data = {
            "email": "22341556@dut4life.ac.za",
            "password": "strong_password_123",
        }
        form = StudentLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.get_user()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "22341556@dut4life.ac.za")

    def test_invalid_login(self):
        form_data = {
            "email": "22341556@dut4life.ac.za",
            "password": "wrong_password",
        }
        form = StudentLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Invalid email or password for a student.", form.errors["__all__"]
        )


class AdminLoginFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="admin@dut4life.ac.za",
            password="strong_password_123",
            is_housing_admin=True,
        )

    def test_valid_login(self):
        form_data = {
            "email": "admin@dut4life.ac.za",
            "password": "strong_password_123",
        }
        form = AdminLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.get_user()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "admin@dut4life.ac.za")

    def test_invalid_login(self):
        form_data = {
            "email": "admin@dut4life.ac.za",
            "password": "wrong_password",
        }
        form = AdminLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Invalid email or password.", form.errors["__all__"])
