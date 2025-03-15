from django.db import models
from django.conf import settings

# Create your models here.

class ProductosAcademicosRelevantes(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descripcion_producto_academico = models.TextField()

    def __str__(self):
        return f"{self.usuario.username} - Producto Académico"
    
    