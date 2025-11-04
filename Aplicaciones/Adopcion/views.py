from django.shortcuts import render, redirect, get_object_or_404
from .models import SolicitudAdopcion
from Aplicaciones.Personas.models import Persona
from Aplicaciones.Mascotas.models import Mascota
from Aplicaciones.autenticacion.decorators import login_required, admin_required
from django.contrib import messages

#extenciones para las graficas
from datetime import date, timedelta
from collections import defaultdict

from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.shortcuts import render



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

        estado_anterior = solicitud.estado
        estado_nuevo = request.POST['estado']

        solicitud.persona_id = request.POST['persona']
        solicitud.mascota_id = request.POST['mascota']
        solicitud.motivo = request.POST['motivo']
        solicitud.estado = estado_nuevo
        
        # primero guardo la solicitud para actualizar relaciones
        solicitud.save()

        # ahora obtengo la mascota correcta
        mascota = solicitud.mascota

        # --- lógica adoptado ---
        if estado_nuevo == "Aprobado":
            mascota.adoptado = True
            mascota.dueño = solicitud.persona
            mascota.save()
            messages.success(request, f'✅ Adopción aprobada. {mascota.nombre} ahora es de {solicitud.persona.nombre}')

        elif estado_anterior == "Aprobado" and estado_nuevo != "Aprobado":
            mascota.adoptado = False
            mascota.dueño = None
            mascota.save()
            messages.info(request, f'🔄 Adopción revertida. {mascota.nombre} está disponible nuevamente')

        return redirect('inicio_adopciones')

    return render(request, 'editar_solicitud.html', {
        'solicitud': solicitud,
        'personas': personas,
        'mascotas': mascotas
    })


@admin_required
def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudAdopcion, id=id)

    # Si la solicitud estaba aprobada, revertimos el estado de la mascota
    if solicitud.estado == "Aprobado":
        mascota = solicitud.mascota
        mascota.adoptado = False
        mascota.dueño = None
        mascota.save()

    # Solo eliminamos la solicitud, no la persona ni la mascota
    solicitud.delete()

    messages.success(request, "🗑️ Solicitud eliminada correctamente.")
    return redirect('inicio_adopciones')



#---------------------------------------------

def dashboard(request):
    # ---- RANGO DE FECHAS (últimos 30 días) ----
    hoy = date.today()
    desde = hoy - timedelta(days=29)
    dias = [desde + timedelta(days=i) for i in range(30)]  # lista ordenada de fechas

    # ---- 1) SERIES: SOLICITUDES POR DÍA Y POR ESTADO ----
    qs = (
        SolicitudAdopcion.objects
        .filter(fecha_solicitud__date__gte=desde, fecha_solicitud__date__lte=hoy)
        .annotate(d=TruncDate('fecha_solicitud'))
        .values('d', 'estado')
        .annotate(total=Count('id'))
        .order_by('d')
    )

    # Estados detectados dinámicamente (por si en el futuro agregas más)
    estados_presentes = list(
        SolicitudAdopcion.objects.values_list('estado', flat=True).distinct()
    ) or ["Pendiente", "Aprobado", "Rechazado"]

    # Mapa: estado -> {fecha -> total}
    mapa = defaultdict(lambda: defaultdict(int))
    for r in qs:
        mapa[r['estado']][r['d']] = r['total']

    # Armamos datasets alineando cada estado contra TODAS las fechas
    labels_fechas = [d.strftime("%d-%m") for d in dias]
    series_por_estado = {}
    for est in estados_presentes:
        serie = [mapa[est][d] for d in dias]
        series_por_estado[est] = serie

    # ---- 2) ADOPTADOS VS NO ADOPTADOS ----
    adoptados_si = Mascota.objects.filter(adoptado=True).count()
    adoptados_no = Mascota.objects.filter(adoptado=False).count()

    # ---- 3) MACHOS VS HEMBRAS ----
    sexos = Mascota.objects.values('sexo').annotate(total=Count('id'))
    sexos_labels = [x['sexo'] or 'No definido' for x in sexos]
    sexos_data = [x['total'] for x in sexos]


    # ---- 4) PREFERENCIA POR ESPECIE (conteo de mascotas por especie) ----
    por_especie = Mascota.objects.values('especie').annotate(total=Count('id'))
    especie_labels = [e['especie'] for e in por_especie]
    especie_data = [e['total'] for e in por_especie]

    # ---- 5) DISTRIBUCIÓN DE EDADES POR ESPECIE (con filtro) ----
    # Rangos: 0-1, 2-4, 5-7, 8-10, 11+
    bucket_labels = ["0-1", "2-4", "5-7", "8-10", "11+"]
    def bucketizar(edad: int) -> int:
        if edad is None: return 0
        if edad <= 1: return 0
        if edad <= 4: return 1
        if edad <= 7: return 2
        if edad <= 10: return 3
        return 4

    especies_distintas = list(Mascota.objects.values_list('especie', flat=True).distinct())
    edades_por_especie = {}
    for esp in especies_distintas:
        cont = [0, 0, 0, 0, 0]
        for edad in Mascota.objects.filter(especie=esp).values_list('edad', flat=True):
            if edad is None: 
                continue
            cont[bucketizar(edad)] += 1
        edades_por_especie[esp] = cont

    # especie seleccionada por query param (?especie=Canina), por defecto la primera
    especie_sel = request.GET.get('especie') or (especies_distintas[0] if especies_distintas else "Canina")
    edades_dataset_actual = edades_por_especie.get(especie_sel, [0, 0, 0, 0, 0])

    context = {
        # linea por día/estado
        "labels_fechas": labels_fechas,
        "estados": estados_presentes,
        "series_por_estado": series_por_estado,

        # adoptados
        "adoptados_labels": ["Adoptadas", "No adoptadas"],
        "adoptados_data": [adoptados_si, adoptados_no],

        # sexos
        "sexos_labels": [s['sexo'] or 'No definido' for s in sexos],
        "sexos_data": sexos_data,

        # especies
        "especie_labels": especie_labels,
        "especie_data": especie_data,

        # edades por especie
        "bucket_labels": bucket_labels,
        "especies_distintas": especies_distintas,
        "especie_sel": especie_sel,
        "edades_por_especie": edades_por_especie,  # mandamos todo para cambiar sin recargar
        "edades_dataset_actual": edades_dataset_actual,
    }
    return render(request, "dashboard.html", context)



from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import os
from django.conf import settings

@login_required
def generar_certificado_adopcion(request, solicitud_id):
    """Genera PDF del certificado de adopción"""
    try:
        # Verificar que la solicitud pertenece al usuario
        persona_usuario = Persona.objects.get(usuario=request.user)
        solicitud = get_object_or_404(SolicitudAdopcion, id=solicitud_id, persona=persona_usuario)
        
        # Solo permitir si está aprobada
        if solicitud.estado != "Aprobada":
            messages.error(request, "Solo puedes generar certificados para adopciones aprobadas")
            return redirect('dashboard_usuario')
        
        # Crear respuesta PDF
        response = HttpResponse(content_type='application/pdf')
        filename = f"certificado_adopcion_{solicitud.mascota.nombre}_{solicitud.persona.nombre}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Crear PDF
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter
        
        # --- ENCABEZADO ---
        p.setFont("Helvetica-Bold", 20)
        p.drawString(100, height - 100, "🐕 CERTIFICADO DE ADOPCIÓN")
        
        # Línea decorativa
        p.setStrokeColorRGB(0.2, 0.6, 0.8)
        p.setLineWidth(2)
        p.line(100, height - 120, width - 100, height - 120)
        
        # --- INFORMACIÓN DE LA MASCOTA ---
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, height - 160, "INFORMACIÓN DE LA MASCOTA:")
        
        p.setFont("Helvetica", 12)
        y_position = height - 190
        info_mascota = [
            f"Nombre: {solicitud.mascota.nombre}",
            f"Especie: {solicitud.mascota.especie}",
            f"Raza: {solicitud.mascota.raza or 'Mixta'}",
            f"Edad: {solicitud.mascota.edad} años",
            f"Sexo: {solicitud.mascota.sexo}",
            f"Descripción: {solicitud.mascota.descripcion or 'Sin descripción adicional'}",
            f"Fecha de Rescate: {solicitud.mascota.fecha_rescate or 'No especificada'}"
        ]
        
        for info in info_mascota:
            p.drawString(120, y_position, info)
            y_position -= 25
        
        # --- INFORMACIÓN DEL ADOPTANTE ---
        y_position -= 20
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y_position, "INFORMACIÓN DEL ADOPTANTE:")
        
        p.setFont("Helvetica", 12)
        y_position -= 30
        info_adoptante = [
            f"Nombre: {solicitud.persona.nombre} {solicitud.persona.apellido}",
            f"Cédula: {solicitud.persona.cedula}",
            f"Correo: {solicitud.persona.correo}",
            f"Teléfono: {solicitud.persona.telefono or 'No registrado'}",
            f"Dirección: {solicitud.persona.direccion}"
        ]
        
        for info in info_adoptante:
            p.drawString(120, y_position, info)
            y_position -= 25
        
        # --- DETALLES DE LA ADOPCIÓN ---
        y_position -= 20
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y_position, "DETALLES DE LA ADOPCIÓN:")
        
        p.setFont("Helvetica", 12)
        y_position -= 30
        info_adopcion = [
            f"Fecha de Solicitud: {solicitud.fecha_solicitud.strftime('%d/%m/%Y')}",
            f"Estado: {solicitud.estado}",
            f"Motivo de Adopción: {solicitud.motivo}"
        ]
        
        for info in info_adopcion:
            p.drawString(120, y_position, info)
            y_position -= 25
        
        # --- FIRMA Y MENSAJE ---
        y_position -= 40
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(100, y_position, "Este documento certifica la adopción responsable de la mascota.")
        y_position -= 20
        p.drawString(100, y_position, "¡Gracias por darle un hogar amoroso!")
        
        # Firma
        y_position -= 60
        p.line(100, y_position, 250, y_position)
        p.setFont("Helvetica", 10)
        p.drawString(100, y_position - 15, "Firma del Sistema de Adopción")
        
        p.showPage()
        p.save()
        
        return response
        
    except Persona.DoesNotExist:
        messages.error(request, "Perfil de usuario no encontrado")
        return redirect('dashboard_usuario')
    except SolicitudAdopcion.DoesNotExist:
        messages.error(request, "Solicitud no encontrada")
        return redirect('dashboard_usuario')