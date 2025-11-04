from django.shortcuts import render, redirect, get_object_or_404
from .models import Mascota
from Aplicaciones.Personas.models import Persona

def inicio(request):
    # Mostrar todas las mascotas
    mascotas = Mascota.objects.all()
    return render(request, 'inicio_mascotas.html', {'mascotas': mascotas})

def nueva_mascota(request):
    # Obtener todas las personas para el dueño
    personas = Persona.objects.all()
    
    if request.method == 'POST':
        # Crear nueva mascota con los datos del formulario
        mascota = Mascota()
        mascota.nombre = request.POST['nombre']
        mascota.especie = request.POST['especie']
        mascota.raza = request.POST['raza']
        mascota.edad = request.POST['edad']
        mascota.sexo = request.POST['sexo']
        mascota.descripcion = request.POST['descripcion']
        mascota.fecha_rescate = request.POST['fecha_rescate']
        
        # Verificar si está adoptado
        if 'adoptado' in request.POST:
            mascota.adoptado = True
        else:
            mascota.adoptado = False
            
        # Asignar dueño si se seleccionó uno
        if request.POST['dueño'] != '':
            dueño = Persona.objects.get(id=request.POST['dueño'])
            mascota.dueño = dueño
            
        mascota.save()
        return redirect('inicio')
    
    return render(request, 'nuevo_mascota.html', {'personas': personas})



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

def eliminar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    mascota.delete()
    return redirect('inicio')