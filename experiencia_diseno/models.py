from django.db import models
from django.conf import settings

# Create your models here.

class ExperienciaDisenoIngenieril(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organismo = models.CharField(max_length=255)
    periodo = models.IntegerField()
    nivel_experiencia = models.CharField(max_length=255)

    def ___str___(self):
        return f"{self.usuario.username} - {self.organismo}"
    