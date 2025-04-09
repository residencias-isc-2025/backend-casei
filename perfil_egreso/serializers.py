from rest_framework import serializers
from perfil_egreso.models import PerfilEgreso

class PerfilEgresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilEgreso
        fields = ['id', 'descripcion', 'carrera']