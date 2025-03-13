from rest_framework import serializers
from institucion.models import InstitucionPais

class InstitucionPaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitucionPais
        fields = ['id', 'nombre_institucion', 'pais', 'estado']

