from django.db import models
from django.conf import settings
from institucion.models import InstitucionPais
from usuarios.models import CustomUser

# Create your models here.

class GestionAcademica(models.Model):
    actividad_puesto = models.CharField(max_length=255)
    institucion_pais = models.ForeignKey(
        InstitucionPais, 
        on_delete=models.CASCADE, 
        related_name='gestion_academica',
        null=True, 
        blank=True
    )
    d_mes_anio = models.DateField()
    a_mes_anio = models.DateField()
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.actividad_puesto} en {self.institucion_pais}"
