from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    document = models.CharField(max_length=100)
    # Otros campos personalizados según sea necesario
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    def __str__(self):
        return self.username

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

class Class(models.Model):
    name = models.CharField(max_length=100)
    required_hours = models.IntegerField()
    level = models.IntegerField()

    def __str__(self):
        return self.name

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student} - {self.class_assigned}"
