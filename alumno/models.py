from django.db import models
from carrera.models import Carrera

class Alumno(models.Model):
    matricula = models.CharField(max_length=100)
    nombre = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='alumnos')

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"