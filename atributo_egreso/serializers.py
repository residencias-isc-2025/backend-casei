from rest_framework import serializers
from atributo_egreso.models import AtributoEgreso
from criterio_desempeno.models import CriterioDesempeno

class AtributoEgresoSerializers(serializers.ModelSerializer):
    criterios_desempeno = serializers.PrimaryKeyRelatedField(
        queryset=CriterioDesempeno.objects.all()
    )

    class Meta:
        model = AtributoEgreso
        fields = ['id', 'descripcion', 'criterios_desempeno']
        