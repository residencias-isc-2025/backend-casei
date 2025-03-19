from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, get_object_or_404
from atributo_egreso.serializers import AtributoEgresoSerializers
from atributo_egreso.models import AtributoEgreso


class AtributoEgresoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todos los atributos de egreso con paginación."""
        atributos = AtributoEgreso.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(atributos, request)
        serializer = AtributoEgresoSerializers(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea un nuevo atributo de egreso."""
        serializer = AtributoEgresoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Atributo de egreso creado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza un atributo de egreso existente."""
        if not pk:
            return Response({"error": "Se requiere un ID de atributo de egreso."}, status=status.HTTP_400_BAD_REQUEST)

        atributo = get_object_or_404(AtributoEgreso, pk=pk)
        serializer = AtributoEgresoSerializers(atributo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Atributo de egreso actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina un atributo de egreso."""
        if not pk:
            return Response({"error": "Se requiere un ID de atributo de egreso."}, status=status.HTTP_400_BAD_REQUEST)

        atributo = get_object_or_404(AtributoEgreso, pk=pk)
        atributo.delete()
        return Response({"mensaje": "Atributo de egreso eliminado correctamente."}, status=status.HTTP_200_OK)

# Create your views here.
