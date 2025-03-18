from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from objetivos_especificos.serializers import ObjetivosEspecificosSerializers
from objetivos_especificos.models import ObjetivosEspecificos
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# Create your views here.

class ObjetivoEspecificoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todos los objetivos específicos con paginación."""
        objetivos = ObjetivosEspecificos.objects.all().order_by('-id')  # <- Quitamos el filtro de usuario
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(objetivos, request)
        serializer = ObjetivosEspecificosSerializers(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea un nuevo objetivo específico."""
        serializer = ObjetivosEspecificosSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Objetivo específico guardado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza un objetivo específico existente."""
        if not pk:
            return Response({"error": "Se requiere un ID de objetivo específico."}, status=status.HTTP_400_BAD_REQUEST)

        objetivo = get_object_or_404(ObjetivosEspecificos, pk=pk)
        serializer = ObjetivosEspecificosSerializers(objetivo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Objetivo específico actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina un objetivo específico."""
        if not pk:
            return Response({"error": "Se requiere un ID de objetivo específico."}, status=status.HTTP_400_BAD_REQUEST)

        objetivo = get_object_or_404(ObjetivosEspecificos, pk=pk)
        objetivo.delete()
        return Response({"mensaje": "Objetivo específico eliminado correctamente."}, status=status.HTTP_200_OK)