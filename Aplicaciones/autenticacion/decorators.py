from django.shortcuts import redirect
from django.contrib import messages
from Aplicaciones.Personas.models import Persona

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión')
            return redirect('login')
        
        try:
            persona = Persona.objects.get(usuario=request.user)
            if not persona.es_admin:
                messages.error(request, 'No tienes permisos de administrador')
                return redirect('dashboard_usuario')
        except Persona.DoesNotExist:
            messages.error(request, 'Perfil de usuario no encontrado')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper