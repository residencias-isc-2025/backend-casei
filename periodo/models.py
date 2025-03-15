from django.db import models

# Create your models here.
class Periodo(models.Model):
    descripcion = models.CharField(max_length=255)
    clave = models.CharField(max_length=20, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.descripcion