from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher, Class, Assignment

def home_view(request):
    return render(request, 'app/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif hasattr(user, 'teacher'):
                return redirect('teacher_dashboard')
            elif hasattr(user, 'student'):
                return redirect('student_dashboard')
        else:
            return render(request, 'app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'app/login.html')

@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('home')
    return render(request, 'app/admin_dashboard.html')

@login_required
def teacher_dashboard_view(request):
    if not hasattr(request.user, 'teacher'):
        return redirect('home')
    return render(request, 'app/teacher_dashboard.html')

@login_required
def student_dashboard_view(request):
    if not hasattr(request.user, 'student'):
        return redirect('home')
    return render(request, 'app/student_dashboard.html')
