from rest_framework import serializers
from usuarios.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'estado', 'apellido_materno', 'apellido_paterno', 'nombre', 
                  'fecha_nacimiento', 'tipo_docente', 'area_adscripcion']
        