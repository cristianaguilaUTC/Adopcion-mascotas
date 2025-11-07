from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Cambiar de '' a 'login/'
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_usuario, name='dashboard_usuario'),
]