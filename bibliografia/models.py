from django.db import models

# Create your models here.
class Bibliografia(models.Model):
    isssn = models.CharField(max_length=100)
    nombre = models.CharField(max_length=255)
    ieee = models.TextField()
    anio = models.IntegerField()
    autor = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.anio})"