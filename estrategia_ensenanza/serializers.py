from rest_framework import serializers
from estrategia_ensenanza.models import EstrategiaEnsenanza

class EstrategiaEnsenanzaSerializers(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEnsenanza
        fields = '__all__'