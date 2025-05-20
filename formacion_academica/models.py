from django.db import models
from usuarios.models import CustomUser
from institucion.models import InstitucionPais
# Create your models here.

class FormacionAcademica(models.Model):
    NIVEL_CHOICES = [
        ('L', 'Licenciatura'),
        ('E', 'Especialidad'),
        ('M', 'Maestría'),
        ('D', 'Doctorado'),
    ]

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="formacion_academica")
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES, null=True, blank=True)  # Solo valores L, E, M, D
    nombre = models.CharField(max_length=255, null=True, blank=True)
    institucion_pais = models.ForeignKey(
        InstitucionPais,
        on_delete=models.CASCADE,
        related_name='formaciones_academicas',
        null=True,
        blank=True
    )
    anio_obtencion = models.IntegerField(null=True, blank=True)
    cedula_profesional = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_nivel_display()}"
