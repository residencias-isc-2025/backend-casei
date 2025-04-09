from django.db import models
from competencia.models import Competencia
from criterio_desempeno.models import CriterioDesempeno
from bibliografia.models import Bibliografia

class Materia(models.Model):
    clave = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    competencias = models.ManyToManyField(Competencia, related_name='materias')
    creditos_requeridos = models.IntegerField(default=0)
    materias_requeridas = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='materias_dependientes')
    semestre = models.CharField(max_length=50)
    tipo_curso = models.BooleanField(help_text='True = Obligatoria, False = Optativa')
    creditos_teoria = models.IntegerField()
    creditos_practica = models.IntegerField()
    horas_ciencias_basicas = models.IntegerField()
    horas_ciencias_ingenieria = models.IntegerField()
    horas_ingenieria_aplicada = models.IntegerField()
    horas_disenio_ingenieril = models.IntegerField()
    horas_ciencias_sociales = models.IntegerField()
    horas_ciencias_economicas = models.IntegerField()
    horas_otros_cursos = models.IntegerField()
    objetivo_general = models.TextField()
    indicador_descripcion = models.TextField()
    criterio_desempeno = models.ManyToManyField(CriterioDesempeno, related_name='materias')
    bibliografia = models.ManyToManyField(Bibliografia, related_name='materias')

    def clean(self):
        total_creditos = self.creditos_teoria + self.creditos_practica
        total_horas = (
            self.horas_ciencias_basicas +
            self.horas_ciencias_ingenieria +
            self.horas_ingenieria_aplicada +
            self.horas_disenio_ingenieril +
            self.horas_ciencias_sociales +
            self.horas_ciencias_economicas +
            self.horas_otros_cursos
        )
        if total_creditos != total_horas:
            from django.core.exceptions import ValidationError
            raise ValidationError("La suma de los créditos no coincide con la suma total de las horas.")

    def __str__(self):
        return f"{self.clave} - {self.nombre}"
    
    