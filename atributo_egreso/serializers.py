from rest_framework import serializers
from atributo_egreso.models import AtributoEgreso

class AtributoEgresoSerializers(serializers.ModelSerializer):
    class Meta:
        model = AtributoEgreso
        fields = ['id', 'siglas', 'descripcion', 'criterios_desempeno']
        extra_kwargs = {
            'criterios_desempeno': {'required': False, 'allow_null': True}
        }
        