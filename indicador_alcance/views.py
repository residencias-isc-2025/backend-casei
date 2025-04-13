from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from indicador_alcance.models import IndicadorAlcance
from indicador_alcance.serializers import IndicadorAlcanceSerializer
from django.shortcuts import get_object_or_404

class IndicadorAlcanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        indicadores = IndicadorAlcance.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(indicadores, request)
        serializer = IndicadorAlcanceSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = IndicadorAlcanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Indicador registrado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        indicador = get_object_or_404(IndicadorAlcance, pk=pk)
        serializer = IndicadorAlcanceSerializer(indicador, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Indicador actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        indicador = get_object_or_404(IndicadorAlcance, pk=pk)
        indicador.delete()
        return Response({'mensaje': 'Indicador eliminado correctamente.'}, status=status.HTTP_200_OK)
    