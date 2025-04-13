from rest_framework import serializers
from sub_temas.models import Subtema

class SubtemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtema
        fields = [
            'id', 'descripcion', 'horas',
            'actividad_aprendizaje', 'estrategia_ensenanza',
            'competencia_generica', 'indicador_alcance',
            'nivel_desempeno', 'lista_cotejo'
        ]