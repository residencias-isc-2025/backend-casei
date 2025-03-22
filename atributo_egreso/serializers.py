from rest_framework import serializers
from atributo_egreso.models import AtributoEgreso

class AtributoEgresoSerializers(serializers.ModelSerializer):
    class Meta:
        model = AtributoEgreso
        fields = ['id', 'siglas', 'descripcion']
        