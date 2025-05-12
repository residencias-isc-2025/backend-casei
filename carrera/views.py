from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from carrera.models import Carrera
from carrera.serializers import CarreraSerializer
from django.shortcuts import get_object_or_404

class CarreraView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            carrera = get_object_or_404(Carrera, pk=pk, is_active=True) 
            serializer = CarreraSerializer(carrera)
            return Response(serializer.data)
        
        paginator = PageNumberPagination()
        
        page_size = request.query_params.get('page_size', 10)
        
        try:
            paginator.page_size = int(page_size)
        except ValueError:
            paginator.page_size = 10

        carreras = Carrera.objects.filter(is_active=True)

        nombre = request.query_params.get('nombre')
        if nombre:
            carreras = carreras.filter(nombre__icontains=nombre)
    
        area_adscripcion = request.query_params.get('area_adscripcion')
        if area_adscripcion:
            carreras = carreras.filter(adscripcion_id=area_adscripcion)

        # Ordenar por ID descendente
        carreras = carreras.order_by('-id')

        # Paginación
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(carreras, request)
        serializer = CarreraSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CarreraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Carrera registrada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)

        carrera = get_object_or_404(Carrera, pk=pk, is_active=True)  
        serializer = CarreraSerializer(carrera, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Carrera actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)

        carrera = get_object_or_404(Carrera, pk=pk)
        carrera.is_active = False
        carrera.save()
