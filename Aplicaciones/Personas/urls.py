from django.urls import path
from . import views

urlpatterns = [
    path('nueva/', views.nueva_persona, name='nueva_persona'),
    path('editar/<int:id>/', views.editar_persona, name='editar_persona'),
    path('eliminar/<int:id>/', views.eliminar_persona, name='eliminar_persona'),
    path('', views.inicio_personas, name='inicio_personas'),  # SIEMPRE AL FINAL
]