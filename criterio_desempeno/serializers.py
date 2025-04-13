from rest_framework import serializers
from criterio_desempeno.models import CriterioDesempeno
from atributo_egreso.models import AtributoEgreso

class CriterioDesempenoSerializers(serializers.ModelSerializer):
    atributo_egreso = serializers.PrimaryKeyRelatedField(
        queryset=AtributoEgreso.objects.all()
    )

    class Meta:
        model = CriterioDesempeno
        fields = ['id', 'atributo_egreso', 'nivel', 'descripcion']

