from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('', views.inicio_adopciones, name='inicio_adopciones'),
    path('nueva/', views.nueva_solicitud, name='nueva_solicitud'),
    path('nueva/<int:mascota_id>/', views.nueva_solicitud, name='nueva_solicitud_con_mascota'),
    path('editar/<int:id>/', views.editar_solicitud, name='editar_solicitud'),
    path('eliminar/<int:id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('certificado/<int:solicitud_id>/', views.generar_certificado_adopcion, name='generar_certificado'),
]
def test_view(request):
    return HttpResponse("✅ ¡APP FUNCIONANDO! El problema son los templates")
