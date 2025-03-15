from rest_framework import serializers
from capacitacion_docente.models import CapacitacionDocente
from institucion.models import InstitucionPais

class CapacitacionDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacitacionDocente
        fields = ['id', 'tipo_capacitacion', 'institucion_pais', 'anio_obtencion', 'horas']

        