from django.db import models
from django.conf import settings
# Create your models here.

class ObjetivosEspecificos(models.Model):
    descripcion = models.TextField()

    def ___str___(self):
        return self.descripcion[:30]