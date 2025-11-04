from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_adopciones, name='inicio_adopciones'),
    path('nueva/', views.nueva_solicitud, name='nueva_solicitud'),
    path('editar/<int:id>/', views.editar_solicitud, name='editar_solicitud'),
    path('eliminar/<int:id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
    path('nueva/<int:mascota_id>/', views.nueva_solicitud, name='nueva_solicitud_con_mascota'),  # ← AGREGAR ESTA

]