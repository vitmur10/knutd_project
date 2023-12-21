from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'IPI',
            'date_of_birth',
            'group',
            'street',
            'house',
            'room',
            'hostel',
            'faculty',
            'course',
            'bloc',
            'learning_from',
            'training_to',
            'passport_series',
            'passport_number',
            'passport_issued',
            'identification_code',
        ]
