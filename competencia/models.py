from django.db import models
from objetivos_especificos.models import ObjetivosEspecificos
from temas.models import Temas

class Competencia(models.Model):
    objetivos_especificos = models.ForeignKey(ObjetivosEspecificos, on_delete=models.CASCADE, related_name='competencias')
    temas = models.ForeignKey(Temas, on_delete=models.CASCADE, related_name='competencias')

    def __str__(self):
        return f"{self.tema} ({self.objetivos_especificos})"

