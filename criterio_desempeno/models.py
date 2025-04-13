from django.db import models
from atributo_egreso.models import AtributoEgreso

# Create your models here.
class CriterioDesempeno(models.Model):
    atributo_egreso = models.ForeignKey(
        AtributoEgreso,
        on_delete=models.CASCADE,
        related_name='criterios_desempeno'
    )
    nivel = models.CharField(max_length=50)
    descripcion=models.TextField()

    def __str__(self):
        return f"{self.nivel} - {self.descripcion[:30]}"
