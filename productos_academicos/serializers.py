from rest_framework import serializers
from productos_academicos.models import ProductosAcademicosRelevantes

class ProductosAcademicosRelevantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductosAcademicosRelevantes
        fields = ['id', 'usuario', 'descripcion_producto_academico']
        read_only_fields = ['usuario']

        