from rest_framework import serializers
from competencia.models import Competencia

class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = ['id', 'objetivos_especificos', 'temas']


        