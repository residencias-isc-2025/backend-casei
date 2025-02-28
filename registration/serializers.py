from rest_framework import serializers
from registration.models import CustomUser, FormacionAcademica

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'apellido_materno', 'apellido_paterno', 'nombre',
                   'fecha_nacimiento', 'tipo_docente']

class FormacionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormacionAcademica
        fields = ['id', 'nivel', 'nombre', 'institucion_pais', 'anio_obtencion', 'cedula_profesional']
        