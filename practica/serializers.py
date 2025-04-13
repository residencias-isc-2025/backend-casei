from rest_framework import serializers
from practica.models import Practica

class PracticaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Practica
        fields = ['id', 'siglas', 'nombre', 'descripcion']

        