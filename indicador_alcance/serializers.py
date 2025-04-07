from rest_framework import serializers
from indicador_alcance.models import IndicadorAlcance

class IndicadorAlcanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorAlcance
        fields = ['id', 'siglas', 'descripcion', 'valor']