from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher, Class

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'document', 'interests']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'document', 'interests']
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'required_hours', 'level']
        # Puedes personalizar los campos si es necesario
