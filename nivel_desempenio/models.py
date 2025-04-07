from django.db import models
from indicador_alcance.models import IndicadorAlcance

class NivelDesempenio(models.Model):
    nombre = models.CharField(max_length=100)
    valor = models.FloatField()
    indicador_alcance = models.ForeignKey(IndicadorAlcance, on_delete=models.CASCADE, related_name='niveles')

    def __str__(self):
        return f"{self.nombre} - {self.valor}"