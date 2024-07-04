from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Incluye las URLs de autenticación por defecto de Django
    path('', include('app.urls')),
]
