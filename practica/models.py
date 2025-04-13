from django.db import models

# Create your models here.
class Practica(models.Model):
    siglas = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.siglas} - {self.nombre}"
    

