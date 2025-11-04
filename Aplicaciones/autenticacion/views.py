from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User  # ← AGREGAR ESTA IMPORTACIÓN
from django.contrib import messages
from Aplicaciones.Personas.models import Persona
from Aplicaciones.Mascotas.models import Mascota
from Aplicaciones.Adopcion.models import SolicitudAdopcion

def login_view(request):
    print("🟢 VISTA LOGIN EJECUTADA")  # ← Esto debe aparecer en terminal
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Verificar si es admin
            try:
                persona = Persona.objects.get(usuario=user)
                if persona.es_admin:
                    return redirect('inicio')  # Admin va a mascotas
            except Persona.DoesNotExist:
                pass
            # Si no es admin o no tiene persona, va al dashboard usuario
            return redirect('dashboard_usuario')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def registro_view(request):
    if request.method == 'POST':
        # Crear usuario
        username = request.POST['username']
        password = request.POST['password']
        correo = request.POST['correo']
        cedula = request.POST['cedula']
        
        # Validaciones
        if len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return render(request, 'registro.html')
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este usuario ya existe')
            return render(request, 'registro.html')
        
        # Verificar si el correo ya existe
        if Persona.objects.filter(correo=correo).exists():
            messages.error(request, 'Este correo ya está registrado')
            return render(request, 'registro.html')
        
        # Verificar si la cédula ya existe
        if Persona.objects.filter(cedula=cedula).exists():
            messages.error(request, 'Esta cédula ya está registrada')
            return render(request, 'registro.html')
        
        try:
            user = User.objects.create_user(username=username, password=password)
            
            # Crear persona
            persona = Persona(
                usuario=user,
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                cedula=cedula,
                correo=correo,
                telefono=request.POST['telefono'],
                direccion=request.POST['direccion'],
                es_admin=False
            )
            persona.save()
            
            # ✅ CAMBIO: Redirigir al login en lugar de autenticar automáticamente
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, 'registro.html')
    
    return render(request, 'registro.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_usuario(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        persona = Persona.objects.get(usuario=request.user)
    except Persona.DoesNotExist:
        messages.error(request, 'Perfil no encontrado')
        return redirect('login')
    
    # ✅ SOLO mascotas NO adoptadas
    mascotas_disponibles = Mascota.objects.filter(adoptado=False)
    
    # Solicitudes del usuario
    solicitudes = SolicitudAdopcion.objects.filter(persona=persona)
    
    return render(request, 'dashboard_usuario.html', {
        'persona': persona,
        'mascotas_disponibles': mascotas_disponibles,  # ← Solo disponibles
        'mascotas_disponibles_count': mascotas_disponibles.count(),  # ← Contador
        'solicitudes': solicitudes,
        'solicitudes_count': solicitudes.count(),  # ← Contador
    })