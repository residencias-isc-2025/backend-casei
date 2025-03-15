from rest_framework import serializers
from experiencia_diseno.models import ExperienciaDisenoIngenieril

class ExperienciaDisenoIngenierilSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaDisenoIngenieril
        fields = ['id', 'usuario', 'organismo', 'periodo', 'nivel_experiencia']
        read_only_fields = ['usuario']
        