from rest_framework import serializers
from adscripcion.models import AreaAdscripcion

class AreaAdscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaAdscripcion
        fields = ['id', 'nombre', 'siglas', 'estado']

