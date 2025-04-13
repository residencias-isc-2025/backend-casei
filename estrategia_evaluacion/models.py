from django.db import models

# Create your models here.
class EstrategiaEvaluacion(models.Model):
    descripcion = models.TextField()

    def ___str___(self):
        return self.descripcion[:30]