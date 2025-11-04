from django.shortcuts import render, redirect
from .models import Mascota
from Aplicaciones.Personas.models import Persona

def inicio(request):
    # Mostrar todas las mascotas
    mascotas = Mascota.objects.all()
    return render(request, 'inicio.html', {'mascotas': mascotas})

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