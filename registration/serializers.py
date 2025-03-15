from rest_framework import serializers
from usuarios.models import CustomUser
from institucion.models import InstitucionPais
"""
class UserSerializer(serializers.ModelSerializer):
    area_adscripcion = serializers.PrimaryKeyRelatedField(
        queryset=AreaAdscripcion.objects.all(), 
        required=False, 
        allow_null=True
    )
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'estado', 'apellido_materno', 'apellido_paterno', 'nombre', 
                  'fecha_nacimiento', 'tipo_docente', 'area_adscripcion']
"""

""""
class InstitucionPaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitucionPais
        fields = ['id', 'nombre_institucion', 'pais', 'estado']
    """    
"""
class CapacitacionDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacitacionDocente
        fields = ['id', 'tipo_capacitacion', 'institucion_pais', 'anio_obtencion', 'horas']
"""


"""
class AreaAdscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaAdscripcion
        fields = ['id', 'nombre', 'siglas', 'estado']
"""
