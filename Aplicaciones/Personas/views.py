from django.shortcuts import render, redirect, get_object_or_404
from .models import Persona
from Aplicaciones.autenticacion.decorators import admin_required

@admin_required
def inicio_personas(request):
    personas = Persona.objects.all()
    return render(request, 'inicio.html', {'personas': personas})

@admin_required
def nueva_persona(request):
    if request.method == 'POST':
        persona = Persona()
        persona.nombre = request.POST['nombre']
        persona.apellido = request.POST['apellido']
        persona.cedula = request.POST['cedula']
        persona.correo = request.POST['correo']
        persona.telefono = request.POST['telefono']
        persona.direccion = request.POST['direccion']

        # ✅ Guardar archivos si se suben
        if 'foto' in request.FILES:
            persona.foto = request.FILES['foto']
        if 'documento_pdf' in request.FILES:
            persona.documento_pdf = request.FILES['documento_pdf']
        
        persona.save()
        return redirect('inicio_personas')
    
    return render(request, 'nuevo_persona.html')


@admin_required
def editar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)

    if request.method == 'POST':
        persona.nombre = request.POST['nombre']
        persona.apellido = request.POST['apellido']
        persona.cedula = request.POST['cedula']
        persona.correo = request.POST['correo']
        persona.telefono = request.POST['telefono']
        persona.direccion = request.POST['direccion']

        # ✅ Si el usuario sube una nueva imagen o PDF, reemplazarlos
        if 'foto' in request.FILES:
            persona.foto = request.FILES['foto']
        if 'documento_pdf' in request.FILES:
            persona.documento_pdf = request.FILES['documento_pdf']

        persona.save()
        return redirect('inicio_personas')

    return render(request, 'editar_persona.html', {'persona': persona})

@admin_required
def eliminar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)
    persona.delete()
    return redirect('inicio_personas')