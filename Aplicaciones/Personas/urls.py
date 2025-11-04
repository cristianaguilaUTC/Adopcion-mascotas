from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_personas, name='inicio_personas'),
    path('nueva/', views.nueva_persona, name='nueva_persona'),
    path('editar/<int:id>/', views.editar_persona, name='editar_persona'),
    path('eliminar/<int:id>/', views.eliminar_persona, name='eliminar_persona'),
]