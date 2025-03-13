from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.
class InstitucionPais(models.Model):
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    )
    
    nombre_institucion = models.CharField(max_length=255)
    pais = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')

    def ___str___(self):
        return f"{self.nombre_institucion} - {self.pais} ({self.get_estado_display()})"
    
    