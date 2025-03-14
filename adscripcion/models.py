from django.db import models

# Create your models here.
class AreaAdscripcion(models.Model):
    nombre = models.CharField(max_length=255)
    siglas = models.CharField(max_length=20)

    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', "Inactivo"),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')

    def __str__(self):
        return f"{self.nombre} ({self.siglas})"