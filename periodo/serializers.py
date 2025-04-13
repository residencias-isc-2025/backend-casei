from rest_framework import serializers
from periodo.models import Periodo

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id', 'clave', 'descripcion', 'fecha_inicio', 'fecha_fin', 'activo']