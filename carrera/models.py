from django.db import models
from adscripcion.models import AreaAdscripcion
from objetivos_especificos.models import ObjetivosEspecificos
from atributo_egreso.models import AtributoEgreso

# Create your models here.
class Carrera(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    adscripcion = models.ForeignKey(
        AreaAdscripcion,
        on_delete=models.CASCADE,
        related_name='adscripcion'
    )
    objetivos_especificos = models.ForeignKey(
        ObjetivosEspecificos,
        on_delete=models.CASCADE,
        related_name='objetivos_espesificos'
    )
    atributos_egreso = models.ManyToManyField(  # Cambiado a ManyToManyField
        AtributoEgreso,
        blank=True,
        related_name='carreras'  # Cambio de 'atributos_egreso' a 'carreras'
    )

    def __str__(self):
        return self.nombre

