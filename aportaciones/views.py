from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from aportaciones.serializers import AportacionSerializer
from aportaciones.models import Aportacion
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.


class AportacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todas las aportaciones del usuario autenticado"""
        aportaciones = Aportacion.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(aportaciones, request)
        serializer = AportacionSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea una nueva aportación para el usuario autenticado"""
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = AportacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Aportación guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza una aportación existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de aportación."}, status=status.HTTP_400_BAD_REQUEST)
        
        aportacion = Aportacion.objects.filter(pk=pk, usuario=request.user).first()
        if not aportacion:
            return Response({"error": "Aportación no encontrada o no tienes permiso para editarla."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AportacionSerializer(aportacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Aportación actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina una aportación existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de aportación."}, status=status.HTTP_400_BAD_REQUEST)
        
        aportacion = Aportacion.objects.filter(pk=pk, usuario=request.user).first()
        if not aportacion:
            return Response({"error": "Aportación no encontrada o no tienes permiso para eliminarla."}, status=status.HTTP_404_NOT_FOUND)

        aportacion.delete()
        return Response({"mensaje": "Aportación eliminada correctamente."}, status=status.HTTP_200_OK)