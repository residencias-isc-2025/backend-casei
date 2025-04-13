from django.db import models
from objetivos_especificos.models import ObjetivosEspecificos
from temas.models import Temas

class Competencia(models.Model):
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    objetivos_especificos = models.ForeignKey(ObjetivosEspecificos, on_delete=models.CASCADE, related_name='competencias')
    temas = models.ManyToManyField(Temas, related_name='competencias')

    def __str__(self):
        return f"{self.tema} ({self.objetivos_especificos})"

