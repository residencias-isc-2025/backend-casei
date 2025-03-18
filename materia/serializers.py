from rest_framework import serializers
from materia.models import Materia
from objetivos_especificos.models import ObjetivosEspecificos
from criterio_desempeno.models import CriterioDesempeno

class MateriaSerializer(serializers.ModelSerializer):
    materias_requeridas = serializers.PrimaryKeyRelatedField(
        queryset=Materia.objects.all(), many=True, required=False
    )
    objetivos_especificos = serializers.PrimaryKeyRelatedField(
        queryset=ObjetivosEspecificos.objects.all(), required=False, allow_null=True
    )
    idcriterio_desempeno = serializers.PrimaryKeyRelatedField(
        queryset=CriterioDesempeno.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Materia
        fields = '__all__'
        