from rest_framework import serializers
from registration.models import CustomUser, FormacionAcademica, NombreProfesor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'tipo_docente']

class FormacionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormacionAcademica
        fields = ['id', 'nivel', 'nombre', 'institucion_pais', 'anio_obtencion', 'cedula_profesional']
        
class NombreProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = NombreProfesor
        fields = ['id', 'apellido_paterno', 'apellido_materno', 'nombre']