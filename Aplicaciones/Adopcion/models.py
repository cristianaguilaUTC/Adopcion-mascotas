from django.db import models

# Create your models here.
from Aplicaciones.Personas.models import Persona
from Aplicaciones.Mascotas.models import Mascota

class SolicitudAdopcion(models.Model):
    id = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='Pendiente')
    motivo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.persona} → {self.mascota} ({self.estado})"