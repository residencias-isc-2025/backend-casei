from rest_framework import serializers
from logros_profesionales.models import LogrosProfesionales


class LogrosProfesionalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogrosProfesionales
        fields = '__all__'