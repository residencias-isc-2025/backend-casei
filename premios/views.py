from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from premios.serializers import PremioSerializer
from premios.models import Premio
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# Create your views here.

class PremioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todos los premios del usuario autenticado"""
        premios = Premio.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(premios, request)
        serializer = PremioSerializer(premios, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea un nuevo premio para el usuario autenticado"""
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = PremioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Premio guardado correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza un premio existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de premio."}, status=status.HTTP_400_BAD_REQUEST)
        
        premio = Premio.objects.filter(pk=pk, usuario=request.user).first()
        if not premio:
            return Response({"error": "Premio no encontrado o no tienes permiso para editarlo."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PremioSerializer(premio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Premio actualizado correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina un premio existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de premio."}, status=status.HTTP_400_BAD_REQUEST)
        
        premio = Premio.objects.filter(pk=pk, usuario=request.user).first()
        if not premio:
            return Response({"error": "Premio no encontrado o no tienes permiso para eliminarlo."}, status=status.HTTP_404_NOT_FOUND)

        premio.delete()
        return Response({"mensaje": "Premio eliminado correctamente."}, status=status.HTTP_200_OK)
    
    