from django.shortcuts import render, redirect, get_object_or_404
from .models import Persona

def inicio_personas(request):
    personas = Persona.objects.all()
    return render(request, 'Personas/inicio.html', {'personas': personas})

def nueva_persona(request):
    if request.method == 'POST':
        persona = Persona()
        persona.nombre = request.POST['nombre']
        persona.apellido = request.POST['apellido']
        persona.cedula = request.POST['cedula']
        persona.correo = request.POST['correo']
        persona.telefono = request.POST['telefono']
        persona.direccion = request.POST['direccion']
        
        persona.save()
        return redirect('inicio_personas')
    
    return render(request, 'Personas/nuevo_persona.html')

def editar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)
    
    if request.method == 'POST':
        persona.nombre = request.POST['nombre']
        persona.apellido = request.POST['apellido']
        persona.cedula = request.POST['cedula']
        persona.correo = request.POST['correo']
        persona.telefono = request.POST['telefono']
        persona.direccion = request.POST['direccion']
        
        persona.save()
        return redirect('inicio_personas')
    
    return render(request, 'Personas/editar_persona.html', {
        'persona': persona
    })

def eliminar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)
    persona.delete()
    return redirect('inicio_personas')