from django import forms
from .models import Application, Student  # Import Application model
from housing.models import Faculty

class ResidenceApplicationForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True)  # This is crucial

    class Meta:
        model = Application
        fields = [
            'faculty',  # Include the faculty field
            # Any other fields that belong to Application
        ]


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 
            'last_name', 
            'student_ID', 
            'home_address_street', 
            'home_address_suburb', 
            'home_address_city', 
            'home_address_postal_code', 
            'faculty', 
            'gender'
        ]
        
    # Optional: Customizing form field attributes (optional, for better UX)
    def __init__(self, *args, **kwargs):
        super(CreateProfileForm, self).__init__(*args, **kwargs)
        
        # Adding placeholders and other attributes
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your first name', 'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your last name', 'class': 'form-control'})
        self.fields['student_ID'].widget.attrs.update({'placeholder': 'Enter your student ID', 'class': 'form-control', 'readonly': 'readonly'})
        # self.fields['cell_number'].widget.attrs.update({'placeholder': 'Enter your cell number', 'class': 'form-control'})
        self.fields['home_address_street'].widget.attrs.update({'placeholder': 'Street name', 'class': 'form-control'})
        self.fields['home_address_suburb'].widget.attrs.update({'placeholder': 'Suburb', 'class': 'form-control'})
        self.fields['home_address_city'].widget.attrs.update({'placeholder': 'City', 'class': 'form-control'})
        self.fields['home_address_postal_code'].widget.attrs.update({'placeholder': 'Postal code', 'class': 'form-control'})
        self.fields['faculty'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        
        # Making the student ID field read-only, as it is linked to the logged-in user
        self.fields['student_ID'].disabled = True


    
