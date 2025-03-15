from django.db import models
from django.conf import settings

# Create your models here.

class ExperienciaProfesionalNoAcademica(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actividad_puesto = models.CharField(max_length=255)
    organizacion_empresa = models.CharField(max_length=255)
    d_mes_anio = models.DateField()
    a_mes_anio = models.DateField()

    def ___str___(self):
        return f"{self.usuario.username} - {self.actividad_puesto}"
    

