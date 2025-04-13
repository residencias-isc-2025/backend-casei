from django.db import models
from actividad_aprendizaje.models import ActividadAprendizaje
from estrategia_ensenanza.models import EstrategiaEnsenanza
from competencias_genericas.models import CompetenciaGenerica
from indicador_alcance.models import IndicadorAlcance
from nivel_desempenio.models import NivelDesempenio
from lista_cotejo.models import ListaCotejo

class Subtema(models.Model):
    descripcion = models.CharField(max_length=255)
    horas = models.IntegerField()
    actividad_aprendizaje = models.ForeignKey(ActividadAprendizaje, on_delete=models.CASCADE, related_name='subtemas')
    estrategia_ensenanza = models.ForeignKey(EstrategiaEnsenanza, on_delete=models.CASCADE, related_name='subtemas')
    competencia_generica = models.ForeignKey(CompetenciaGenerica, on_delete=models.CASCADE, related_name='subtemas')
    indicador_alcance = models.ForeignKey(IndicadorAlcance, on_delete=models.CASCADE, related_name='subtemas')
    nivel_desempeno = models.ForeignKey(NivelDesempenio, on_delete=models.CASCADE, related_name='subtemas')
    lista_cotejo = models.ForeignKey(ListaCotejo, on_delete=models.CASCADE, related_name='subtemas')

    def __str__(self):
        return self.descripcion