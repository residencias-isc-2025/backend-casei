from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from actividad_aprendizaje.models import ActividadAprendizaje
from actividad_aprendizaje.serializers import ActividadAprendizajeSerializer
from django.shortcuts import get_object_or_404

class ActividadAprendizajeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        actividades = ActividadAprendizaje.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(actividades, request)
        serializer = ActividadAprendizajeSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ActividadAprendizajeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Actividad registrada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        actividad = get_object_or_404(ActividadAprendizaje, pk=pk)
        serializer = ActividadAprendizajeSerializer(actividad, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Actividad actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        actividad = get_object_or_404(ActividadAprendizaje, pk=pk)
        actividad.delete()
        return Response({'mensaje': 'Actividad eliminada correctamente.'}, status=status.HTTP_200_OK)