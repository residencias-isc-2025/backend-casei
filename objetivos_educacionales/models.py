from django.db import models
from carrera.models import Carrera

class ObjetivoEducacional(models.Model):
    descripcion = models.CharField(max_length=500)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='objetivos_educacionales')

    def __str__(self):
        return f"{self.descripcion[:50]}..."