from django.db import models

class ListaCotejo(models.Model):
    nombre = models.CharField(max_length=255)
    actividad = models.FileField(upload_to='listas_cotejo/')

    def __str__(self):
        return self.nombre