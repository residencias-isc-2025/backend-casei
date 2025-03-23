from rest_framework import serializers
from temas.models import Temas

class TemasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Temas
        fields = ['id', 'nombre', 'objetivo', 'criterio_desempeno', 'estrategia_ensenanza', 'estrategia_evaluacion', 'practica']


