from django.db import models

# Create your models here.
from Aplicaciones.Personas.models import Persona

class Mascota(models.Model):
  
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=100, blank=True, null=True)
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_rescate = models.DateField(blank=True, null=True)
    adoptado = models.BooleanField(default=False)
    dueño = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True, related_name='mascotas')
    foto = models.ImageField(upload_to='fotos_mascotas/', blank=True, null=True)
    documento = models.FileField(upload_to='documentos_mascotas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.especie})"