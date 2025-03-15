from rest_framework import serializers
from premios.models import Premio

class PremioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premio
        fields = '__all__'

        