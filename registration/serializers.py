from rest_framework import serializers
from registration.models import CustomUser, FormacionAcademica, InstitucionPais, CapacitacionDocente, ActualizacionDisciplinaria

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'apellido_materno', 'apellido_paterno', 'nombre',
                   'fecha_nacimiento', 'tipo_docente']

class FormacionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormacionAcademica
        fields = ['id', 'nivel', 'nombre', 'institucion_pais', 'anio_obtencion', 'cedula_profesional']

class InstitucionPaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitucionPais
        fields = ['id', 'nombre_institucion', 'pais']
        
class CapacitacionDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacitacionDocente
        fields = ['id', 'tipo_capacitacion', 'institucion_pais', 'año_obtencion', 'horas']

class ActualizacionDisciplinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualizacionDisciplinaria
        fields = ['id', 'tipo_actualizacion', 'institucion_pais', 'año_obtencion', 'horas']
