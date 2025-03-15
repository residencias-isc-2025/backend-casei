from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from actualizacion_diciplinar.serializers import ActualizacionDisciplinarSerializer
from actualizacion_diciplinar.models import ActualizacionDisciplinaria
from institucion.models import InstitucionPais
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.

class ActualizacionDisciplinarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Devuelve las actualizaciones disciplinarias del usuario autenticado"""
        paginator = PageNumberPagination()
        paginator.page_size = 10
        if pk:
            actualizacion = get_object_or_404(ActualizacionDisciplinaria, pk=pk, usuario=request.user)
            serializer = ActualizacionDisciplinarSerializer(actualizacion)
            return Response(serializer.data)
        
        actualizaciones = ActualizacionDisciplinaria.objects.filter(usuario=request.user).order_by('anio_obtencion')
        result_page = paginator.paginate_queryset(actualizaciones, request)
        serializer = ActualizacionDisciplinarSerializer(result_page, many=True)        
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea una nueva actualización disciplinar para el usuario autenticado"""
        serializer = ActualizacionDisciplinarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({"mensaje": "Actualización disciplinar registrada correctamente.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza una actualización disciplinar existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de actualización disciplinar."}, status=status.HTTP_400_BAD_REQUEST)

        actualizacion = get_object_or_404(ActualizacionDisciplinaria, pk=pk, usuario=request.user)
        serializer = ActualizacionDisciplinarSerializer(actualizacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Actualización disciplinar actualizada correctamente.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina una actualización disciplinar existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de actualización disciplinar."}, status=status.HTTP_400_BAD_REQUEST)

        actualizacion = get_object_or_404(ActualizacionDisciplinaria, pk=pk, usuario=request.user)
        actualizacion.delete()
        return Response({"mensaje": "Actualización disciplinar eliminada correctamente."}, status=status.HTTP_200_OK)

