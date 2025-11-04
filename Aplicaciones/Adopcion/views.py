from django.shortcuts import render, redirect, get_object_or_404
from .models import SolicitudAdopcion
from Aplicaciones.Personas.models import Persona
from Aplicaciones.Mascotas.models import Mascota
from Aplicaciones.autenticacion.decorators import login_required, admin_required
from django.contrib import messages


from Aplicaciones.autenticacion.decorators import login_required

@login_required
def solicitar_adopcion_usuario(request, mascota_id):
    """Vista para que usuarios normales soliciten adopción"""
    try:
        persona_usuario = Persona.objects.get(usuario=request.user)
        mascota = get_object_or_404(Mascota, id=mascota_id, adoptado=False)
    except Persona.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado')
        return redirect('dashboard_usuario')
    
    if request.method == 'POST':
        solicitud = SolicitudAdopcion()
        solicitud.persona = persona_usuario
        solicitud.mascota = mascota
        solicitud.motivo = request.POST['motivo']
        solicitud.estado = 'Pendiente'
        solicitud.save()
        
        messages.success(request, f'✅ Solicitud enviada para {mascota.nombre}')
        return redirect('dashboard_usuario')
    
    return render(request, 'solicitar_adopcion.html', {
        'mascota': mascota,
        'persona': persona_usuario
    })

@admin_required
def inicio_adopciones(request):
    solicitudes = SolicitudAdopcion.objects.all().select_related('persona', 'mascota')
    return render(request, 'inicio_adopciones.html', {'solicitudes': solicitudes})

@login_required
def nueva_solicitud(request, mascota_id=None):
    if mascota_id:
        mascota = get_object_or_404(Mascota, id=mascota_id)
        mascotas = Mascota.objects.filter(id=mascota_id)
    else:
        mascota = None
        mascotas = Mascota.objects.filter(adoptado=False)
    
    # Para usuarios normales, solo pueden solicitar para sí mismos
    try:
        persona_usuario = Persona.objects.get(usuario=request.user)
        personas = Persona.objects.filter(id=persona_usuario.id)
    except Persona.DoesNotExist:
        personas = Persona.objects.none()
    
    if request.method == 'POST':
        solicitud = SolicitudAdopcion()
        solicitud.persona_id = request.POST['persona']
        solicitud.mascota_id = request.POST['mascota']
        solicitud.motivo = request.POST['motivo']
        solicitud.estado = 'Pendiente'
        
        solicitud.save()
        return redirect('dashboard_usuario')
    
    return render(request, 'nueva_solicitud.html', {
        'personas': personas,
        'mascotas': mascotas,
        'mascota_seleccionada': mascota
    })

@admin_required
def editar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudAdopcion, id=id)
    personas = Persona.objects.all()
    mascotas = Mascota.objects.all()
    
    if request.method == 'POST':
        solicitud.persona_id = request.POST['persona']
        solicitud.mascota_id = request.POST['mascota']
        solicitud.motivo = request.POST['motivo']
        solicitud.estado = request.POST['estado']
        
        solicitud.save()
        return redirect('inicio_adopciones')
    
    return render(request, 'editar_solicitud.html', {
        'solicitud': solicitud,
        'personas': personas,
        'mascotas': mascotas
    })

@admin_required
def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudAdopcion, id=id)
    solicitud.delete()
    return redirect('inicio_adopciones')