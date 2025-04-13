from rest_framework import serializers
from donde_trabaja.models import DondeTrabaja

class DondeTrabajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DondeTrabaja
        fields = ['id', 'descripcion', 'carrera']