from django.db import models
from django.conf import settings
from institucion.models import InstitucionPais

# Create your models here.

class ActualizacionDisciplinaria(models.Model):
    tipo_actualizacion = models.CharField(max_length=255)
    institucion_pais = models.ForeignKey(
        InstitucionPais, 
        on_delete=models.CASCADE, 
        related_name='actualizaciones_disciplinarias',
        null=True, 
        blank=True
    )
    anio_obtencion = models.PositiveIntegerField()
    horas = models.PositiveIntegerField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actualizacion_disciplinar')

    def __str__(self):
        return f"{self.tipo_actualizacion} - {self.usuario.username}"
    
