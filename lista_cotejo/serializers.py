from rest_framework import serializers
from lista_cotejo.models import ListaCotejo

class ListaCotejoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaCotejo
        fields = ['id', 'nombre', 'actividad']