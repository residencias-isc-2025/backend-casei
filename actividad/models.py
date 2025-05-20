from django.db import models
from alumno.models import Alumno
from calificaciones.models import Calificacion

def evidencia_path(instance, filename):
    return f'actividades/evidencias/{instance.pk}/{filename}'

def formato_path(instance, filename):
    return f'actividades/formatos/{instance.pk}/{filename}'

class Actividad(models.Model):
    descripcion = models.FileField(upload_to='actividades/descripcion/', null=True, blank=True)
    formato = models.FileField(upload_to=formato_path, null=True, blank=True)
    
    calificaciones = models.ManyToManyField(Calificacion, blank=True, related_name='actividades')

    alumno_alto = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='actividades_alto', null=True, blank=True)
    alumno_alto_calificacion = models.FloatField(null=True, blank=True)
    alumno_alto_evidencia = models.FileField(upload_to=evidencia_path, null=True, blank=True)

    alumno_promedio = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='actividades_promedio', null=True, blank=True)
    alumno_promedio_calificacion = models.FloatField(null=True, blank=True)
    alumno_promedio_evidencia = models.FileField(upload_to=evidencia_path, null=True, blank=True)

    alumno_bajo = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='actividades_bajo', null=True, blank=True)
    alumno_bajo_calificacion = models.FloatField(null=True, blank=True)
    alumno_bajo_evidencia = models.FileField(upload_to=evidencia_path, null=True, blank=True)

    def __str__(self):
        return f"Actividad #{self.id}"