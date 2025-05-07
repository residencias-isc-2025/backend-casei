from rest_framework import serializers
from carrera.models import Carrera

class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = ['id', 'nombre', 'adscripcion', 'objetivos_especificos', 'atributos_egreso', 'mision', 'vision', 'objetivo_carrera', 'is_active']

        
