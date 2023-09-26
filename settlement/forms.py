from django import forms
from .models import Student, StudentParens


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['IPI', 'group', 'street', 'house', 'room', 'hostel', 'faculty', 'course', 'learning_from',
                  'training_to', 'passport_series', 'passport_number', 'passport_issued', 'identification_code',
                  'date_of_birth']


class StudentParentsForm(forms.ModelForm):
    class Meta:
        model = StudentParens
        fields = ['IPIF', 'passport_series_f', 'passport_number_f', 'passport_issued_f']
