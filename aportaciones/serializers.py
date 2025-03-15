from rest_framework import serializers
from aportaciones.models import Aportacion

class AportacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aportacion
        fields = '__all__'

        