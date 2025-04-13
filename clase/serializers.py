from rest_framework import serializers
from clase.models import Clase

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = ['id', 'grupo', 'materia', 'carrera', 'periodo', 'alumnos']