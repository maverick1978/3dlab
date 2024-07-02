from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher, Class, Assignment, CustomUser
from .forms import ClassForm, CreateUserForm
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages

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

def create_class_view(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app/admin_dashboard')  # Ajusta la redirección según sea necesario
    else:
        form = ClassForm()
    
    return render(request, 'app/create_class.html', {'form': form})

@login_required
def admin_dashboard_view(request):
    form_user = CreateUserForm()
    form_class = ClassForm()
    if not request.user.is_superuser:
        return redirect('home')
    return render(request, 'app/admin_dashboard.html', {'form_user': form_user, 'form_class': form_class})


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

def create_class_view(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ClassForm()
    return render(request, 'app/create_class.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('app/login')
    
def create_user_popup_view(request):
    form = CreateUserForm()
    return render(request, 'app/create_user.html', {'form': form})

def create_class_popup_view(request):
    form = ClassForm()
    return render(request, 'app/create_class.html', {'form': form})

def create_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        user_type = request.POST['user_type']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('admin_dashboard')  # O redirigir a otra vista adecuada

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.user_type = user_type
        user.save()

        if user_type == 'student':
            Student.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)
        elif user_type == 'teacher':
            Teacher.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)

        messages.success(request, 'User created successfully!')
        return redirect('admin_dashboard')  # Redirigir a una vista adecuada después de la creación

    return HttpResponse("Crear usuario aquí")  # Puedes cambiar esto a una redirección o renderizado de template
def assign_students_view(request):
    if request.method == 'POST':
        # Lógica para procesar el formulario y asignar estudiantes a clases
        # Ejemplo básico:
        student_id = request.POST.get('student')
        class_id = request.POST.get('class')
        student = Student.objects.get(pk=student_id)
        class_instance = Class.objects.get(pk=class_id)
        # Asignación de estudiante a clase (aquí deberías definir la lógica según tu aplicación)
        # Por ejemplo:
        class_instance.students.add(student)
        class_instance.save()
        return redirect('teacher_dashboard')  # Redirige a donde corresponda

    # Renderiza el formulario inicial si es un GET request
    students = Student.objects.all()
    classes = Class.objects.all()
    context = {'students': students, 'classes': classes}
    return render(request, 'app/assign_student.html', context)
