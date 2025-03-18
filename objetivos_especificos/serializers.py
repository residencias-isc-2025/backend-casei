from rest_framework import serializers
from objetivos_especificos.models import ObjetivosEspecificos

class ObjetivosEspecificosSerializers(serializers.ModelSerializer):
    class Meta:
        model = ObjetivosEspecificos
        fields = '__all__'