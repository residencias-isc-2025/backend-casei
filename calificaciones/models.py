from django.db import models
from alumno.models import Alumno
from clase.models import Clase
# NO IMPORTES actividad.models directamente aquí

class Calificacion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='calificaciones')
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='calificaciones')
    actividad = models.ForeignKey('actividad.Actividad', on_delete=models.SET_NULL, null=True, blank=True, related_name='calificaciones_directas')
    calificacion = models.IntegerField()

    def __str__(self):
        return f"{self.alumno} - {self.clase} ({self.calificacion})"