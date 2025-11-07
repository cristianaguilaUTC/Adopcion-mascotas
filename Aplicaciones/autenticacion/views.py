from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from Aplicaciones.Personas.models import Persona
from Aplicaciones.Mascotas.models import Mascota
from Aplicaciones.Adopcion.models import SolicitudAdopcion

def login_view(request):
    print("🟢 VISTA LOGIN EJECUTADA")
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
                    return redirect('/mascotas/')  # ← CORRECTO
            except Persona.DoesNotExist:
                pass
            # Si no es admin o no tiene persona, va al dashboard usuario
            return redirect('dashboard_usuario')  # ← CORREGIDO: quitar 'request'
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'autenticacion/login.html')  # ← CAMBIAR: agregar 'autenticacion/'

def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        correo = request.POST['correo']
        cedula = request.POST['cedula']
        
        if len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return render(request, 'autenticacion/registro.html')  # ← CAMBIAR
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este usuario ya existe')
            return render(request, 'autenticacion/registro.html')  # ← CAMBIAR
        
        if Persona.objects.filter(correo=correo).exists():
            messages.error(request, 'Este correo ya está registrado')
            return render(request, 'autenticacion/registro.html')  # ← CAMBIAR
        
        if Persona.objects.filter(cedula=cedula).exists():
            messages.error(request, 'Esta cédula ya está registrada')
            return render(request, 'autenticacion/registro.html')  # ← CAMBIAR
        
        try:
            user = User.objects.create_user(username=username, password=password)
            
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
            
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión')
            return redirect('login')  # ← ESTA ESTÁ BIEN
            
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, 'autenticacion/registro.html')  # ← CAMBIAR
    
    return render(request, 'autenticacion/registro.html')  # ← CAMBIAR

def logout_view(request):
    logout(request)
    return redirect('/auth/login/')  # ← CAMBIAR: usar ruta completa

def dashboard_usuario(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')  # ← CAMBIAR: usar ruta completa
    
    try:
        persona = Persona.objects.get(usuario=request.user)
    except Persona.DoesNotExist:
        messages.error(request, 'Perfil no encontrado')
        return redirect('/auth/login/')  # ← CAMBIAR: usar ruta completa
    
    mascotas_disponibles = Mascota.objects.filter(adoptado=False)
    solicitudes = SolicitudAdopcion.objects.filter(persona=persona)
    
    return render(request, 'autenticacion/dashboard_usuario.html', {  # ← CAMBIAR
        'persona': persona,
        'mascotas_disponibles': mascotas_disponibles,
        'mascotas_disponibles_count': mascotas_disponibles.count(),
        'solicitudes': solicitudes,
        'solicitudes_count': solicitudes.count(),
    })