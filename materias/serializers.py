from rest_framework import serializers
from materias.models import Materia

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = [
            'id',
            'clave',
            'nombre',
            'competencias',
            'creditos_requeridos',
            'materias_requeridas',
            'semestre',
            'tipo_curso',
            'creditos_teoria',
            'creditos_practica',
            'horas_ciencias_basicas',
            'horas_ciencias_ingenieria',
            'horas_ingenieria_aplicada',
            'horas_disenio_ingenieril',
            'horas_ciencias_sociales',
            'horas_ciencias_economicas',
            'horas_otros_cursos',
            'objetivo_general',
            'indicador_descripcion',
            'criterio_desempeno',
            'bibliografia'
        ]

    def validate(self, data):
        creditos_teoria = data.get('creditos_teoria', 0)
        creditos_practica = data.get('creditos_practica', 0)
        total_creditos = creditos_teoria + creditos_practica

        horas_totales = (
            data.get('horas_ciencias_basicas', 0) +
            data.get('horas_ciencias_ingenieria', 0) +
            data.get('horas_ingenieria_aplicada', 0) +
            data.get('horas_disenio_ingenieril', 0) +
            data.get('horas_ciencias_sociales', 0) +
            data.get('horas_ciencias_economicas', 0) +
            data.get('horas_otros_cursos', 0)
        )

        if total_creditos != horas_totales:
            raise serializers.ValidationError("La suma de los créditos no coincide con la suma total de las horas.")
        return data
    
    