from rest_framework import serializers
from clase.models import Clase

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = ['id', 'docente', 'grupo', 'materia', 'carrera', 'periodo', 'alumnos']

    def validate_docente(self, value):
        if value is not None and value.role not in ['user', 'docentee']:
            raise serializers.ValidationError("El usuario asignado como docente debe tener rol 'user' o 'docentee'.")
        return value
    