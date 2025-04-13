from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from perfil_ingreso.models import PerfilIngreso
from perfil_ingreso.serializers import PerfilIngresoSerializer
from django.shortcuts import get_object_or_404

class PerfilIngresoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        perfiles = PerfilIngreso.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(perfiles, request)
        serializer = PerfilIngresoSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PerfilIngresoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Perfil de ingreso registrado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        perfil = get_object_or_404(PerfilIngreso, pk=pk)
        serializer = PerfilIngresoSerializer(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Perfil de ingreso actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        perfil = get_object_or_404(PerfilIngreso, pk=pk)
        perfil.delete()
        return Response({'mensaje': 'Perfil de ingreso eliminado correctamente.'}, status=status.HTTP_200_OK)