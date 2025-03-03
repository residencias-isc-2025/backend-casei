from rest_framework import serializers
from registration.models import CustomUser, FormacionAcademica, InstitucionPais, CapacitacionDocente, ActualizacionDisciplinaria, GestionAcademica, ProductosAcademicosRelevantes, ExperienciaProfesionalNoAcademica, ExperienciaDisenoIngenieril, LogrosProfesionales, Participacion, Premio, Aportacion

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
        fields = ['id', 'tipo_capacitacion', 'institucion_pais', 'anio_obtencion', 'horas']

class ActualizacionDisciplinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualizacionDisciplinaria
        fields = ['id', 'tipo_actualizacion', 'institucion_pais', 'anio_obtencion', 'horas']

class GestionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionAcademica
        fields = ['id', 'actividad_puesto', 'institucion_pais', 'd_mes_anio', 'a_mes_anio', 'usuario']

class ProductosAcademicosRelevantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductosAcademicosRelevantes
        fields = ['id', 'usuario', 'descripcion_producto_academico']
        read_only_fields = ['usuario']

class ExperienciaProfesionalNoAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaProfesionalNoAcademica
        fields = ['id', 'usuario', 'actividad_puesto', 'organizacion_empresa', 'd_mes_anio', 'a_mes_anio']
        read_only_fields = ['usuario']

class ExperienciaDisenoIngenierilSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaDisenoIngenieril
        fields = ['id', 'usuario', 'organismo', 'periodo', 'nivel_experiencia']
        read_only_fields = ['usuario']

class LogrosProfesionalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogrosProfesionales
        fields = '__all__'

class ParticipacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participacion
        fields = '__all__'

class PremioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premio
        fields = '__all__'

class AportacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aportacion
        fields = '__all__'

