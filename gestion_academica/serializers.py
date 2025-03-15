from rest_framework import serializers
from gestion_academica.models import GestionAcademica
from institucion.models import InstitucionPais

class GestionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionAcademica
        fields = ['id', 'actividad_puesto', 'institucion_pais', 'd_mes_anio', 'a_mes_anio', 'usuario']
        
