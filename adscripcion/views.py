from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from adscripcion.models import AreaAdscripcion
from adscripcion.serializers import AreaAdscripcionSerializer

# Create your views here.
class AreaAdscripcionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Devuelve las áreas de adscripción, con paginación y tamaño de página dinámico"""
        paginator = PageNumberPagination()
        
        # Permitir que el usuario defina el tamaño de la página desde los parámetros de consulta
        page_size = request.query_params.get('page_size', 10)  # Valor predeterminado de 10
        try:
            paginator.page_size = int(page_size)
        except ValueError:
            paginator.page_size = 10  # Valor predeterminado si el parámetro no es un número válido

        if pk:
            area = get_object_or_404(AreaAdscripcion, pk=pk)
            serializer = AreaAdscripcionSerializer(area)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Parámetros de búsqueda
        search_nombre = request.query_params.get('nombre', None)
        search_siglas = request.query_params.get('siglas', None)
        search_estado = request.query_params.get('estado', None)

        # Consulta base
        areas = AreaAdscripcion.objects.all().order_by('nombre')

        # Aplicar filtros condicionales
        if search_nombre:
            areas = areas.filter(nombre__icontains=search_nombre)
        if search_siglas:
            areas = areas.filter(siglas__iexact=search_siglas)
        if search_estado:
            areas = areas.filter(estado__iexact=search_estado)

        # Paginación
        result_page = paginator.paginate_queryset(areas, request)
        serializer = AreaAdscripcionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea una nueva área de adscripción"""
        serializer = AreaAdscripcionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Área de adscripción creada correctamente.", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza los datos de un área de adscripción"""
        if not pk:
            return Response({"error": "Se requiere un ID para actualizar el área de adscripción."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        area = get_object_or_404(AreaAdscripcion, pk=pk)
        serializer = AreaAdscripcionSerializer(area, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Área de adscripción actualizada correctamente.", "data": serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Inhabilita (marca como inactiva) un área de adscripción en lugar de eliminarla"""
        if not pk:
            return Response({"error": "Se requiere un ID para inhabilitar el área de adscripción."},
                            status=status.HTTP_400_BAD_REQUEST)

        area = get_object_or_404(AreaAdscripcion, pk=pk)
        area.estado = 'inactivo'
        area.save()

        return Response({"mensaje": f"Área de adscripción marcada como inactiva correctamente."},
                        status=status.HTTP_200_OK)
    
class HabilitarAreaAdscripcionView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        """Habilita un área de adscripción previamente marcada como inactiva."""
        if not pk:
            return Response({"error": "Se requiere un ID de área de adscripción para habilitarla."},
                            status=status.HTTP_400_BAD_REQUEST)

        area = get_object_or_404(AreaAdscripcion, pk=pk)

        if area.estado == 'activo':
            return Response({"mensaje": f"El área de adscripción ya está activa."},
                            status=status.HTTP_400_BAD_REQUEST)

        area.estado = 'activo'
        area.save()

        return Response({"mensaje": f"Área de adscripción habilitada correctamente."},
                        status=status.HTTP_200_OK)
