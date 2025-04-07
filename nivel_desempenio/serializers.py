from rest_framework import serializers
from nivel_desempenio.models import NivelDesempenio

class NivelDesempenioSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelDesempenio
        fields = ['id', 'nombre', 'valor', 'indicador_alcance']