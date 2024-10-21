from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register the custom user model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_student', 'is_housing_admin', 'student_id', 'is_active', 'is_staff')
    list_filter = ('is_student', 'is_housing_admin', 'is_active', 'is_staff')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

