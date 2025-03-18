from rest_framework import serializers
from criterio_desempeno.models import CriterioDesempeno

class CriterioDesempenoSerializers(serializers.ModelSerializer):
    class Meta:
        model = CriterioDesempeno
        fields = '__all__'

