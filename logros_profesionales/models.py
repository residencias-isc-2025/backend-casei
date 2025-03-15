from django.db import models
from django.conf import settings
from usuarios.models import CustomUser

# Create your models here.

class LogrosProfesionales(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def ___str___(self):
        return f"{self.usuario.username} - {self.descripcion[:30]}..."