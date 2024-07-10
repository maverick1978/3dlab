from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib import messages
from .models import Student, Teacher, Class, Assignment, CustomUser, Resource
from .forms import ClassForm, CreateUserForm, ResourceForm, StudentForm, TeacherForm
from .utils import is_teacher, is_student, is_admin  # Asegúrate de importar is_admin

# Definición de las funciones is_teacher, is_student e is_admin
def is_teacher(user):
    return hasattr(user, 'teacher')

def is_student(user):
    return hasattr(user, 'student')

def is_admin(user):
    return user.is_superuser

# Resto de las vistas
def home_view(request):
    return render(request, 'app/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"Authenticated user: {user.username}")  # Debugging print statement
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or None
            if next_url:
                print(f"Redirecting to next URL: {next_url}")  # Debugging print statement
                return redirect(next_url)
            elif user.is_superuser:
                print("Redirecting to admin dashboard")  # Debugging print statement
                return redirect('admin_dashboard')
            elif hasattr(user, 'teacher'):
                print("Redirecting to teacher dashboard")  # Debugging print statement
                return redirect('teacher_dashboard')
            elif hasattr(user, 'student'):
                print("Redirecting to student dashboard")  # Debugging print statement
                return redirect('student_dashboard')
            else:
                print("User does not have permissions for any dashboard")  # Debugging print statement
                messages.error(request, 'No tiene permiso para acceder a este sitio.')
                logout(request)
                return redirect('login')
        else:
            print("Authentication failed")  # Debugging print statement
            messages.error(request, 'Credenciales no válidas.')
    return render(request, 'app/login.html', {'next': request.GET.get('next', '')})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    form_user = CreateUserForm()
    form_class = ClassForm()
    classes = Class.objects.all()  # Asegúrate de obtener las clases
    return render(request, 'app/admin_dashboard.html', {'form_user': form_user, 'form_class': form_class, 'classes': classes})

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    return render(request, 'app/teacher_dashboard.html')

@login_required
@user_passes_test(is_student)
def student_dashboard_view(request):
    return render(request, 'app/student_dashboard.html')

@login_required
@user_passes_test(is_admin)
def create_class_view(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ClassForm()
    return render(request, 'app/create_class.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_class_view(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ClassForm(instance=cls)
    return render(request, 'app/edit_class.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_class_view(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        class_instance.delete()
        return redirect('admin_dashboard')
    return render(request, 'app/delete_class.html', {'class': class_instance})

@login_required
@user_passes_test(lambda u: is_teacher(u) or is_student(u))
def view_class_view(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    resources = Resource.objects.filter(class_resource=cls).order_by('level')
    return render(request, 'app/view_class.html', {'class': cls, 'resources': resources})

@login_required
@user_passes_test(is_teacher)
def add_resource_view(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.class_resource = cls
            resource.save()
            return redirect('view_class', class_id=class_id)
    else:
        form = ResourceForm()
    return render(request, 'app/add_resource.html', {'form': form, 'class': cls})

@login_required
@user_passes_test(is_admin)
def create_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        user_type = request.POST['user_type']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('admin_dashboard')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('admin_dashboard')

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.user_type = user_type
        user.save()

        if user_type == 'student':
            Student.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)
        elif user_type == 'teacher':
            Teacher.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)

        messages.success(request, 'User created successfully!')
        return redirect('admin_dashboard')

    return HttpResponse("Crear usuario aquí")

@login_required
@user_passes_test(is_teacher)
def assign_students_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        class_id = request.POST.get('class')
        student = Student.objects.get(pk=student_id)
        class_instance = Class.objects.get(pk=class_id)
        class_instance.students.add(student)
        class_instance.save()
        return redirect('teacher_dashboard')

    students = Student.objects.all()
    classes = Class.objects.all()
    context = {'students': students, 'classes': classes}
    return render(request, 'app/assign_student.html', context)
@login_required
def edit_user_view(request):
    if request.user.is_student:
        student = get_object_or_404(Student, user=request.user)
        if request.method == 'POST':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Datos del estudiante actualizados con éxito.')
                return redirect('student_dashboard')
        else:
            form = StudentForm(instance=student)
    elif request.user.is_teacher:
        teacher = get_object_or_404(Teacher, user=request.user)
        if request.method == 'POST':
            form = TeacherForm(request.POST, instance=teacher)
            if form.is_valid():
                form.save()
                messages.success(request, 'Datos del profesor actualizados con éxito.')
                return redirect('teacher_dashboard')
        else:
            form = TeacherForm(instance=teacher)
    else:
        messages.error(request, 'No tiene permiso para editar estos datos.')
        return redirect('home')

    return render(request, 'app/edit_user.html', {'form': form})

def confirm_delete_class(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        class_instance.delete()
        return redirect('admin_dashboard')  # Ajusta según tu URL
    return render(request, 'app/admin_dashboard.html', {'class': class_instance})

def delete_class(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        class_instance.delete()
        return redirect('admin_dashboard')
    return render(request, 'app/admin_dashboard.html')
