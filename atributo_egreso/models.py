from django.db import models
from criterio_desempeno.models import CriterioDesempeno

# Create your models here.

class AtributoEgreso(models.Model):
    descripcion = models.TextField()
    criterios_desempeno = models.ForeignKey(
        CriterioDesempeno,
        on_delete=models.CASCADE,
        related_name='atributos_egreso'
    )

    def __str__(self):
        return self.descripcion
