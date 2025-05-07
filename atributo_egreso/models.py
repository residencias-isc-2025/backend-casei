from django.db import models

# Create your models here.
class AtributoEgreso(models.Model):
    siglas = models.CharField(max_length=10, unique=True, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.siglas
    
