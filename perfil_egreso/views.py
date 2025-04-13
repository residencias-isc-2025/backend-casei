from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from perfil_egreso.models import PerfilEgreso
from perfil_egreso.serializers import PerfilEgresoSerializer
from django.shortcuts import get_object_or_404

class PerfilEgresoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        perfiles = PerfilEgreso.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(perfiles, request)
        serializer = PerfilEgresoSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PerfilEgresoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Perfil de egreso registrado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        perfil = get_object_or_404(PerfilEgreso, pk=pk)
        serializer = PerfilEgresoSerializer(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Perfil de egreso actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        perfil = get_object_or_404(PerfilEgreso, pk=pk)
        perfil.delete()
        return Response({'mensaje': 'Perfil de egreso eliminado correctamente.'}, status=status.HTTP_200_OK)