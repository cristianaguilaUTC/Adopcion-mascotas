from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=15, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    es_admin = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='personas/fotos/', null=True, blank=True)
    documento_pdf = models.FileField(upload_to='personas/documentos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"