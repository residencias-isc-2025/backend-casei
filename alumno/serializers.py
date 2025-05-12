from rest_framework import serializers
from alumno.models import Alumno

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['id', 'matricula', 'nombre', 'apellido_materno', 'apellido_paterno', 'carrera', 'is_active']