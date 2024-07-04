from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    required_hours = models.IntegerField(null=True, blank=True)
    level = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=255, null=True, blank=True) 
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Cambia related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_user_permissions',  # Cambia related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document = models.CharField(max_length=100)
    interests = models.TextField()
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document = models.CharField(max_length=100)
    interests = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    required_hours = models.IntegerField()
    level = models.CharField(max_length=100, choices=[(str(i), str(i)) for i in range(1, 5)])  # Limitar a 4 niveles

    def __str__(self):
        return self.name


class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student} - {self.class_assigned}"
    
class Resource(models.Model):
    class_resource = models.ForeignKey(Class, on_delete=models.CASCADE)
    level = models.CharField(max_length=50)
    text = models.TextField()
    pdf = models.FileField(upload_to='resources/pdfs/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
