from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher, Class, CustomUser, Resource

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
#class ClassForm(forms.ModelForm):
 #   class Meta:
  #      model = Class
   #     fields = ['name', 'required_hours', 'level']
        # Puedes personalizar los campos si es necesario

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'user_type']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'description', 'start_date', 'end_date', 'required_hours', 'level']
        widgets = {
            'required_hours': forms.NumberInput(attrs={'min': 1, 'max': 20}),
        }
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['level', 'text', 'pdf', 'video_url']