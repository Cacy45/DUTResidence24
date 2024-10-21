from django import forms
from housing.models import Residence, Room, HousingAdmin, Faculty
from student.models import Application


# Purpose: To create or update residence details.
class ResidenceForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True)  # This is crucial

    class Meta:
        model = Residence
        fields = ['residence_name', 'residence_address', 'total_num_of_rooms', 'distance_to_campus', 'faculty']
        widgets = {
            'residence_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'residence_address': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'total_num_of_rooms': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'distance_to_campus': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),  # Change to NumberInput
            'faculty': forms.Select(attrs={'class': 'form-control'})
        }
        
# Purpose: To create or update details about individual rooms in a residence.
class RoomAssignmentForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.none(), label="Select Room")

    def __init__(self, *args, **kwargs):
        preferred_room_type = kwargs.pop('preferred_room_type', None)
        super().__init__(*args, **kwargs)
        
        # Filter the queryset based on the preferred room type
        if preferred_room_type:
            self.fields['room'].queryset = Room.objects.filter(room_type=preferred_room_type, available_beds__gt=0)
'''
# Purpose: To handle student applications for residence.
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['application_date', 'status', 'student', 'residence']
        exclude =['application_date']
        widgets = {
            # 'application_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'residence': forms.Select(attrs={'class': 'form-control'}),
        }
        '''


class HousingAdminForm(forms.ModelForm):
    class Meta:
        model = HousingAdmin
        fields = ['first_name', 'last_name', 'cell_number']  # Exclude 'user' since it will be set in the view
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cell_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


'''
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['student', 'admin', 'submission_date', 'status']  # include any fields you want
        widgets = {
            'submission_date': forms.DateInput(attrs={'type': 'date'}),
        }
'''

'''
class ResidenceForm(forms.ModelForm):
    class Meta:
        model = Residence
        fields = ['residence_name', 'residence_address', 'total_num_of_rooms', 'distance_to_campus']
        widgets = {
            'residence_name': forms.TextInput(attrs={'class': 'form-control'}),
            'residence_address': forms.TextInput(attrs={'class': 'form-control'}),
            'total_num_of_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'distance_to_campus': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_total_num_of_rooms(self):
        total_num_of_rooms = self.cleaned_data.get('total_num_of_rooms')
        if total_num_of_rooms <= 0:
            raise forms.ValidationError("Total number of rooms must be greater than zero.")
        return total_num_of_rooms

    def clean_distance_to_campus(self):
        distance_to_campus = self.cleaned_data.get('distance_to_campus')
        if distance_to_campus < 0:
            raise forms.ValidationError("Distance to campus cannot be negative.")
        return distance_to_campus
'''
    
# Purpose: To assign a room to a student from available rooms.
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'bed_count', 'available_beds']
        widgets = {
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'bed_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_beds': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_bed_count(self):
        bed_count = self.cleaned_data.get('bed_count')
        if bed_count <= 0:
            raise forms.ValidationError("Bed count must be greater than zero.")
        return bed_count

    def clean_available_beds(self):
        available_beds = self.cleaned_data.get('available_beds')
        if available_beds < 0:
            raise forms.ValidationError("Available beds cannot be negative.")
        return available_beds

    # Optional: Add a clean method to ensure available_beds does not exceed bed_count
    def clean(self):
        cleaned_data = super().clean()
        bed_count = cleaned_data.get('bed_count')
        available_beds = cleaned_data.get('available_beds')

        if available_beds is not None and bed_count is not None and available_beds > bed_count:
            raise forms.ValidationError("Available beds cannot exceed total bed count.")


'''
# Purpose: To handle student applications for residence.
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['submission_date', 'status', 'student', 'admin']
        exclude = ['application_date']  # Exclude the non-editable field
        widgets = {
            'submission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'admin': forms.Select(attrs={'class': 'form-control'}),
        }
'''
'''
# Purpose: To create or update details for housing administrators.
class HousingAdminForm(forms.ModelForm):
    class Meta:
        model = HousingAdmin
        fields = ['admin_id', 'first_name', 'last_name', 'cell_number', 'user']
        widgets = {
            'admin_id': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cell_number': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }
'''