from rest_framework import serializers
from estrategia_evaluacion.models import EstrategiaEvaluacion

class EstrategiaEvaluacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEvaluacion
        fields = '__all__'