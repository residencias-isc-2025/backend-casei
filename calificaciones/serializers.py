from rest_framework import serializers
from calificaciones.models import Calificacion

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['id', 'alumno', 'clase', 'actividad', 'calificacion']