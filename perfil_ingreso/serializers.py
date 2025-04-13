from rest_framework import serializers
from perfil_ingreso.models import PerfilIngreso

class PerfilIngresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilIngreso
        fields = ['id', 'descripcion', 'carrera']