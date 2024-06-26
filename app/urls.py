from django.urls import path
from .views import create_class_view,home_view, create_user_view, login_view, admin_dashboard_view, teacher_dashboard_view, student_dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('teacher_dashboard/', teacher_dashboard_view, name='teacher_dashboard'),
    path('student_dashboard/', student_dashboard_view, name='student_dashboard'),
    path('create_user/', create_user_view, name='create_user'),
    path('create_class/', create_class_view, name='create_class'),
]
