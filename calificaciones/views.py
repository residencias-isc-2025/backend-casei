from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from calificaciones.models import Calificacion
from calificaciones.serializers import CalificacionSerializer
from clase.models import Clase
from clase.serializers import ClaseSerializer
from django.shortcuts import get_object_or_404

class CalificacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        calificaciones = Calificacion.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(calificaciones, request)
        serializer = CalificacionSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CalificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Calificación registrada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        calificacion = get_object_or_404(Calificacion, pk=pk)
        serializer = CalificacionSerializer(calificacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Calificación actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        calificacion = get_object_or_404(Calificacion, pk=pk)
        calificacion.delete()
        return Response({'mensaje': 'Calificación eliminada correctamente.'}, status=status.HTTP_200_OK)
    
class CalificacionesPorClaseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clase_id):
        clase = get_object_or_404(Clase, pk=clase_id)
        calificaciones = Calificacion.objects.filter(clase=clase).order_by('-id')
        serializer = CalificacionSerializer(calificaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    