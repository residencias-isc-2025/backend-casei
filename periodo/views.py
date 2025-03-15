from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from periodo.models import Periodo
from periodo.serializers import PeriodoSerializer

# Create your views here.
class PeriodoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        paginator = PageNumberPagination()
        page_size = request.query_params.get('page_size', 10)
        
        try:
            paginator.page_size = int(page_size)
        except ValueError:
            paginator.page_size = 10
            
        if pk:
            periodo = get_object_or_404(Periodo, pk=pk)
            serializer = PeriodoSerializer(periodo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        search_clave = request.query_params.get('clave', None)
        search_activo = request.query_params.get('activo', None)
        
        periodos = Periodo.objects.all().order_by('fecha_fin')
        
        if search_clave:
            periodos = periodos.filter(clave__startswith=search_clave)
        if search_activo:
            periodos = periodos.filter(activo__iexact=search_activo)
            
        result_page = paginator.paginate_queryset(periodos, request)
        serializer = PeriodoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = PeriodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Periodo creado correctamente.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID para actualizar el periodo"}, status=status.HTTP_400_BAD_REQUEST)

        periodo = get_object_or_404(Periodo, pk=pk)
        serializer = PeriodoSerializer(periodo, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Periodo actualizado correctamente."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID para desactivar el periodo"}, status=status.HTTP_400_BAD_REQUEST)
        
        periodo = get_object_or_404(Periodo, pk=pk)
        periodo.activo = False
        periodo.save()
        
        return Response({'mensaje': 'Periodo desactivado correctamente.'}, status=status.HTTP_200_OK)
    
class ActivarPeriodoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID para activar el periodo"}, status=status.HTTP_400_BAD_REQUEST)
        
        periodo = get_object_or_404(Periodo, pk=pk)
        periodo.activo = True
        periodo.save()
        
        return Response({'mensaje': 'Periodo activado correctamente.'}, status=status.HTTP_200_OK)
    