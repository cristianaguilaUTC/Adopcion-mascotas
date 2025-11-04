from django.shortcuts import render, redirect, get_object_or_404
from .models import Mascota
from Aplicaciones.Personas.models import Persona
from Aplicaciones.autenticacion.decorators import login_required, admin_required

@login_required
def inicio(request):
    mascotas = Mascota.objects.all()
    return render(request, 'inicio_mascotas.html', {'mascotas': mascotas})

@admin_required
def nueva_mascota(request):
    personas = Persona.objects.all()
    
    if request.method == 'POST':
        mascota = Mascota()
        mascota.nombre = request.POST['nombre']
        mascota.especie = request.POST['especie']
        mascota.raza = request.POST['raza']
        mascota.edad = request.POST['edad']
        mascota.sexo = request.POST['sexo']
        mascota.descripcion = request.POST['descripcion']
        mascota.fecha_rescate = request.POST['fecha_rescate']
        
        if 'adoptado' in request.POST:
            mascota.adoptado = True
        else:
            mascota.adoptado = False
            
        if request.POST['dueño'] != '':
            dueño = Persona.objects.get(id=request.POST['dueño'])
            mascota.dueño = dueño
            
        mascota.save()
        return redirect('inicio')
    
    return render(request, 'nuevo_mascota.html', {'personas': personas})

@admin_required
def editar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    personas = Persona.objects.all()
    
    if request.method == 'POST':
        mascota.nombre = request.POST['nombre']
        mascota.especie = request.POST['especie']
        mascota.raza = request.POST['raza']
        mascota.edad = request.POST['edad']
        mascota.sexo = request.POST['sexo']
        mascota.descripcion = request.POST['descripcion']
        mascota.fecha_rescate = request.POST['fecha_rescate']
        mascota.adoptado = 'adoptado' in request.POST
        
        if request.POST['dueño'] != '':
            dueño = Persona.objects.get(id=request.POST['dueño'])
            mascota.dueño = dueño
        else:
            mascota.dueño = None
            
        mascota.save()
        return redirect('inicio')
    
    return render(request, 'editar_mascota.html', {
        'mascota': mascota,
        'personas': personas
    })

@admin_required
def eliminar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    mascota.delete()
    return redirect('inicio')