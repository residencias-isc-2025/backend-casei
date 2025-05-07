from django.db import models
from carrera.models import Carrera

class Alumno(models.Model):
    matricula = models.CharField(max_length=100, null=True, blank=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    apellido_materno = models.CharField(max_length=255, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=255, null=True, blank=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='alumnos', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.matricula or 'Sin matrícula'} - {self.nombre or 'Sin nombre'}"