from rest_framework import serializers
from participacion.models import Participacion

class ParticipacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participacion
        fields = '__all__'

