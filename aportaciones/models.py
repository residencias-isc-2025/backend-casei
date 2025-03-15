from django.db import models
from django.conf import settings

# Create your models here.

class Aportacion(models.Model):
    descripcion = models.CharField(max_length=255)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descripcion[:30]}..."
    
    