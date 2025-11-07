from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect

def test_view(request):
    return HttpResponse("✅ ¡La app funciona! El problema está en los templates o static files")

def home(request):
    return redirect('/auth/login/')  # Redirige al login automáticamente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # ← AGREGAR ESTA LÍNEA (ruta principal)
    path('test/', test_view),
    path('auth/', include('Aplicaciones.autenticacion.urls')),
    path('mascotas/', include('Aplicaciones.Mascotas.urls')),
    path('personas/', include('Aplicaciones.Personas.urls')),
    path('adopciones/', include('Aplicaciones.Adopcion.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)