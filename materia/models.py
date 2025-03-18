from django.db import models
from objetivos_especificos.models import ObjetivosEspecificos
from criterio_desempeno.models import CriterioDesempeno

class Materia(models.Model):
    clave = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    creditos_requeridos = models.IntegerField(default=0, blank=True, null=True)

    materias_requeridas = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='materias_dependientes'
    )

    semestre = models.CharField(max_length=50)
    tipo_curso = models.CharField(
        max_length=20, 
        choices=[('obligatorio', 'Obligatorio'), ('optativo', 'Optativo')]
    )

    creditos_teoria = models.IntegerField()
    creditos_practica = models.IntegerField()

    horas_ciencias_basicas = models.IntegerField()
    horas_ciencias_ingenieria = models.IntegerField()
    horas_ingenieria_aplicada = models.IntegerField()
    horas_diseno_ingeniril = models.IntegerField()
    horas_ciencias_sociales = models.IntegerField()
    horas_ciencias_economicas = models.IntegerField()
    horas_otros_cursos = models.IntegerField()

    objetivo_general = models.TextField()
    indicador_descripcion = models.TextField()

    # Relación con `ObjetivosEspecificos` siguiendo el modelo de `gestion_academica`
    objetivos_especificos = models.ForeignKey(
        ObjetivosEspecificos,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materias"
    )

    idcriterio_desempeno = models.ForeignKey(
        CriterioDesempeno,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        total_horas = (
            self.horas_ciencias_basicas + self.horas_ciencias_ingenieria +
            self.horas_ingenieria_aplicada + self.horas_diseno_ingeniril +
            self.horas_ciencias_sociales + self.horas_ciencias_economicas +
            self.horas_otros_cursos
        )
        if self.creditos_teoria + self.creditos_practica != total_horas:
            raise ValueError("La suma de créditos de teoría y práctica debe ser igual a la suma de todas las horas.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre