from django.db import models

# Create your models here.
class IndicadorAlcance(models.Model):
    siglas = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    valor = models.FloatField()

    def __str__(self):
        return f"{self.siglas} - {self.valor}"
    