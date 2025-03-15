from rest_framework import serializers
from experiencia_profesional.models import ExperienciaProfesionalNoAcademica


class ExperienciaProfesionalNoAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaProfesionalNoAcademica
        fields = ['id', 'usuario', 'actividad_puesto', 'organizacion_empresa', 'd_mes_anio', 'a_mes_anio']
        read_only_fields = ['usuario']

