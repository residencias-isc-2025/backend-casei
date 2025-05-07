from django.db import models
from adscripcion.models import AreaAdscripcion
from objetivos_especificos.models import ObjetivosEspecificos
from atributo_egreso.models import AtributoEgreso

class Carrera(models.Model):
    nombre = models.CharField(max_length=255)
    adscripcion = models.ForeignKey(AreaAdscripcion, on_delete=models.CASCADE, related_name='carreras', null=True, blank=True)
    objetivo_especifico = models.ManyToManyField(ObjetivosEspecificos, related_name='carreras', blank=True)
    atributos_egreso = models.ManyToManyField(AtributoEgreso, related_name='carreras', blank=True)
    mision = models.TextField(null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
    objetivo_carrera = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    
