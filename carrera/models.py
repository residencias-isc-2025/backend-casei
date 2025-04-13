from django.db import models
from adscripcion.models import AreaAdscripcion
from objetivos_especificos.models import ObjetivosEspecificos
from atributo_egreso.models import AtributoEgreso

class Carrera(models.Model):
    nombre = models.CharField(max_length=255)
    adscripcion = models.ForeignKey(AreaAdscripcion, on_delete=models.CASCADE, related_name='carreras')
    objetivo_especifico = models.ForeignKey(ObjetivosEspecificos, on_delete=models.CASCADE, related_name='carreras')
    atributos_egreso = models.ManyToManyField(AtributoEgreso, related_name='carreras')

    def __str__(self):
        return self.nombre
    
