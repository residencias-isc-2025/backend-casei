from rest_framework import serializers
from competencias_genericas.models import CompetenciaGenerica

class CompetenciaGenericaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetenciaGenerica
        fields = ['id', 'descripcion']