from rest_framework import serializers
from actividad_aprendizaje.models import ActividadAprendizaje


class ActividadAprendizajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadAprendizaje
        fields = ['id', 'descripcion']


