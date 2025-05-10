from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from clase.models import Clase
from clase.serializers import ClaseSerializer
from django.shortcuts import get_object_or_404

class ClaseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            clase = get_object_or_404(Clase, pk=pk) 
            serializer = ClaseSerializer(clase)
            return Response(serializer.data)
        
        clases = Clase.objects.all()
        
        grupo = request.query_params.get('grupo')
        if grupo:
            clases = clases.filter(grupo=grupo)

        materia = request.query_params.get('materia')
        if materia:
            clases = clases.filter(materia_id=materia)

        carrera = request.query_params.get('carrera')
        if carrera:
            clases = clases.filter(carrera_id=carrera)

        periodo = request.query_params.get('periodo')
        if periodo:
            clases = clases.filter(periodo_id=periodo)

        clases = clases.order_by('-id')

        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(clases, request)
        serializer = ClaseSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ClaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Clase registrada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        clase = get_object_or_404(Clase, pk=pk)
        serializer = ClaseSerializer(clase, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Clase actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        clase = get_object_or_404(Clase, pk=pk)
        clase.delete()
        return Response({'mensaje': 'Clase eliminada correctamente.'}, status=status.HTTP_200_OK)
    