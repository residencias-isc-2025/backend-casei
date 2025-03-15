from rest_framework import serializers
from actualizacion_diciplinar.models import ActualizacionDisciplinaria
from usuarios.models import CustomUser
from institucion.models import InstitucionPais

class ActualizacionDisciplinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualizacionDisciplinaria
        fields = ['id', 'tipo_actualizacion', 'institucion_pais', 'anio_obtencion', 'horas']

