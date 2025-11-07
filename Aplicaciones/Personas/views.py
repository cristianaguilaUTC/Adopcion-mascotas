from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Persona
from Aplicaciones.autenticacion.decorators import admin_required

@admin_required
def inicio_personas(request):
    personas = Persona.objects.all()
    return render(request, 'inicio.html', {'personas': personas})

@admin_required
def nueva_persona(request):
    if request.method == 'POST':
        # Tu código actual de nueva persona
        persona = Persona()
        persona.nombre = request.POST['nombre']
        persona.apellido = request.POST['apellido']
        persona.cedula = request.POST['cedula']
        persona.correo = request.POST['correo']
        persona.telefono = request.POST['telefono']
        persona.direccion = request.POST['direccion']

        if 'foto' in request.FILES:
            persona.foto = request.FILES['foto']
        if 'documento_pdf' in request.FILES:
            persona.documento_pdf = request.FILES['documento_pdf']
        
        persona.save()
        messages.success(request, 'Persona creada correctamente.')
        return redirect('inicio_personas')
    
    return render(request, 'nuevo_persona.html')

@admin_required
def editar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)
    if request.method == 'POST':
        # Tu código actual de editar
        persona.nombre = request.POST['nombre']
        persona.apellido = request.POST['apellido']
        persona.cedula = request.POST['cedula']
        persona.correo = request.POST['correo']
        persona.telefono = request.POST['telefono']
        persona.direccion = request.POST['direccion']

        if 'foto' in request.FILES:
            persona.foto = request.FILES['foto']
        if 'documento_pdf' in request.FILES:
            persona.documento_pdf = request.FILES['documento_pdf']

        persona.save()
        messages.success(request, 'Persona actualizada correctamente.')
        return redirect('inicio_personas')

    return render(request, 'editar_persona.html', {'persona': persona})

@admin_required
def eliminar_persona(request, id):
    if request.method == 'POST':
        persona = get_object_or_404(Persona, id=id)
        nombre_completo = f"{persona.nombre} {persona.apellido}"
        
        try:
            # ✅ VALIDACIÓN: Evitar que el admin se elimine a sí mismo
            if persona.usuario == request.user:
                messages.error(request, 'No puedes eliminar tu propio perfil de administrador.')
                return redirect('inicio_personas')
            
            # Verificar relaciones de forma SEGURA
            from Aplicaciones.Mascotas.models import Mascota
            from Aplicaciones.Adopcion.models import SolicitudAdopcion
            
            # ✅ VALIDACIÓN MEJORADA: Verificar relaciones foráneas
            tiene_mascotas = Mascota.objects.filter(dueño=persona).exists()
            tiene_solicitudes = SolicitudAdopcion.objects.filter(persona=persona).exists()
            
            if tiene_mascotas or tiene_solicitudes:
                mensaje_error = f'No se puede eliminar a {nombre_completo} porque tiene '
                if tiene_mascotas and tiene_solicitudes:
                    mensaje_error += 'mascotas y solicitudes de adopción relacionadas.'
                elif tiene_mascotas:
                    mensaje_error += 'mascotas relacionadas.'
                else:
                    mensaje_error += 'solicitudes de adopción relacionadas.'
                
                messages.error(request, mensaje_error)
            else:
                # Si no hay relaciones, eliminar también el usuario de Django
                if persona.usuario:
                    persona.usuario.delete()
                persona.delete()
                messages.success(request, f'Persona {nombre_completo} eliminada correctamente.')
                
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('inicio_personas')