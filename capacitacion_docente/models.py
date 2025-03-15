from django.db import models
from django.conf import settings
from institucion.models import InstitucionPais
# Create your models here.

class CapacitacionDocente(models.Model):
    tipo_capacitacion = models.CharField(max_length=255)
    institucion_pais = models.ForeignKey(
        InstitucionPais, 
        on_delete=models.CASCADE, 
        related_name='capacitaciones',
        null=True, 
        blank=True
    )
    anio_obtencion = models.PositiveIntegerField()
    horas = models.PositiveIntegerField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='capacitaciones_docentes')

    def ___str___(self):
        return f"{self.tipo_capacitacion} - {self.usuario.username}"