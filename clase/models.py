from django.db import models
from materias.models import Materia
from carrera.models import Carrera
from periodo.models import Periodo
from alumno.models import Alumno

class Clase(models.Model):
    GRUPO_CHOICES = [
        ('01', 'Grupo 01'),
        ('02', 'Grupo 02'),
        ('03', 'Grupo 03'),
    ]

    grupo = models.CharField(max_length=2, choices=GRUPO_CHOICES)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='clases')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='clases')
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='clases')
    alumnos = models.ManyToManyField(Alumno, related_name='clases')

    def __str__(self):
        return f"{self.materia.nombre} - Grupo {self.grupo} - {self.periodo}"