from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import assign_students_view, create_user_view, add_resource_view, view_class_view, delete_class_view, home_view, login_view, logout_view, admin_dashboard_view, teacher_dashboard_view, student_dashboard_view, create_class_view,edit_class_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('teacher_dashboard/',teacher_dashboard_view, name='teacher_dashboard'),
    path('student_dashboard/',student_dashboard_view, name='student_dashboard'),
    path('create_class/', create_class_view, name='create_class'),
    path('edit_class/<int:class_id>/', edit_class_view, name='edit_class'),
    path('delete_class/<int:class_id>/',delete_class_view, name='delete_class'),
    path('view_class/<int:class_id>/', view_class_view, name='view_class'),
    path('add_resource/<int:class_id>/', add_resource_view, name='add_resource'),
    path('create_user/', create_user_view, name='create_user'),
    path('assign_students/', assign_students_view, name='assign_students'),
    path('', home_view, name='home'),
]
