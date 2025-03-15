from django.db import models
from django.conf import settings
from usuarios.models import CustomUser
# Create your models here.

class Participacion(models.Model):
    organismo = models.CharField(max_length=255)
    periodo = models.IntegerField()
    nivel_p = models.CharField(max_length=255)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organismo} - {self.periodo}"