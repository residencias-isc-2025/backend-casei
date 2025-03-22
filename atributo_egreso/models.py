from django.db import models

# Create your models here.
class AtributoEgreso(models.Model):
    siglas = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.siglas
    