from django.db import models
from criterio_desempeno.models import CriterioDesempeno
from estrategia_ensenanza.models import EstrategiaEnsenanza
from estrategia_evaluacion.models import EstrategiaEvaluacion
from practica.models import Practica

class Temas(models.Model):
    nombre = models.CharField(max_length=255)
    objetivo = models.TextField()
    
    criterio_desempeno = models.ForeignKey(
        CriterioDesempeno,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='temas'
    )
    estrategia_ensenanza = models.ForeignKey(
        EstrategiaEnsenanza,
        on_delete=models.CASCADE,
        related_name='temas'
    )
    estrategia_evaluacion = models.ForeignKey(
        EstrategiaEvaluacion,
        on_delete=models.CASCADE,
        related_name='temas'
    )
    practica = models.ForeignKey(
        Practica,
        on_delete=models.CASCADE,
        related_name='temas'
    )

    def __str__(self):
        return self.nombre