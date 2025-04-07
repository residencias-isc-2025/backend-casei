from rest_framework import serializers
from bibliografia.models import Bibliografia

class BibliografiaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bibliografia
        fields = ['id', 'isssn', 'nombre', 'ieee', 'anio', 'autor', 'tipo']

