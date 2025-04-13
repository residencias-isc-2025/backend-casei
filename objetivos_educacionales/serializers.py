from rest_framework import serializers
from objetivos_educacionales.models import ObjetivoEducacional

class ObjetivoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEducacional
        fields = ['id', 'descripcion', 'carrera']