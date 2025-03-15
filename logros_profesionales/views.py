from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from logros_profesionales.serializers import LogrosProfesionalesSerializer
from logros_profesionales.models import LogrosProfesionales
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.

class LogroProfesionalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todos los logros profesionales del usuario autenticado."""
        logros = LogrosProfesionales.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(logros, request)
        serializer = LogrosProfesionalesSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea un nuevo logro profesional para el usuario autenticado."""
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = LogrosProfesionalesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Logro profesional guardado correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza un logro profesional existente del usuario autenticado."""
        if not pk:
            return Response({"error": "Se requiere un ID de logro profesional."}, status=status.HTTP_400_BAD_REQUEST)

        logro = get_object_or_404(LogrosProfesionales, pk=pk, usuario=request.user)
        data = request.data.copy()
        data['usuario'] = request.user.id

        serializer = LogrosProfesionalesSerializer(logro, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Logro profesional actualizado correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina un logro profesional del usuario autenticado."""
        if not pk:
            return Response({"error": "Se requiere un ID de logro profesional."}, status=status.HTTP_400_BAD_REQUEST)

        logro = get_object_or_404(LogrosProfesionales, pk=pk, usuario=request.user)
        logro.delete()
        return Response({"mensaje": "Logro profesional eliminado correctamente."}, status=status.HTTP_200_OK)
    