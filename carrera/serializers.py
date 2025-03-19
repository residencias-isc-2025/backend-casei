from rest_framework import serializers
from carrera.models import Carrera
from adscripcion.models import AreaAdscripcion
from objetivos_especificos.models import ObjetivosEspecificos
from atributo_egreso.models import AtributoEgreso

class CarreraSerializer(serializers.ModelSerializer):
    adscripcion = serializers.PrimaryKeyRelatedField(
        queryset=AreaAdscripcion.objects.all()
    )
    objetivos_especificos = serializers.PrimaryKeyRelatedField(
        queryset=ObjetivosEspecificos.objects.all()
    )
    atributos_egreso = serializers.PrimaryKeyRelatedField(
        queryset=AtributoEgreso.objects.all(),
        many=True,  # Ahora es una lista de IDs porque es ManyToManyField
        required=False
    )

    class Meta:
        model = Carrera
        fields = ['id', 'nombre', 'adscripcion', 'objetivos_especificos', 'atributos_egreso']

    def create(self, validated_data):
        atributos_egreso_data = validated_data.pop('atributos_egreso', [])
        carrera = Carrera.objects.create(**validated_data)
        carrera.atributos_egreso.set(atributos_egreso_data)  # Asignar atributos de egreso
        return carrera
    
    