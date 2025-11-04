from django.shortcuts import render, redirect, get_object_or_404
from .models import SolicitudAdopcion
from Aplicaciones.Personas.models import Persona
from Aplicaciones.Mascotas.models import Mascota

def inicio_adopciones(request):
    solicitudes = SolicitudAdopcion.objects.all().select_related('persona', 'mascota')
    return render(request, 'inicio_adopciones.html', {'solicitudes': solicitudes})

def nueva_solicitud(request):
    personas = Persona.objects.all()
    mascotas = Mascota.objects.filter(adoptado=False)  # Solo mascotas no adoptadas
    
    if request.method == 'POST':
        solicitud = SolicitudAdopcion()
        solicitud.persona_id = request.POST['persona']
        solicitud.mascota_id = request.POST['mascota']
        solicitud.motivo = request.POST['motivo']
        solicitud.estado = 'Pendiente'
        
        solicitud.save()
        return redirect('inicio_adopciones')
    
    return render(request, 'nueva_solicitud.html', {
        'personas': personas,
        'mascotas': mascotas
    })

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

def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudAdopcion, id=id)
    solicitud.delete()
    return redirect('inicio_adopciones')