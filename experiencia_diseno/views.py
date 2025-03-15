from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from django.shortcuts import render
from experiencia_diseno.serializers import ExperienciaDisenoIngenierilSerializer
from experiencia_diseno.models import ExperienciaDisenoIngenieril
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# Create your views here.

class ExperienciaDisenoIngenierilView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: Listar todas las experiencias en diseño ingenieril del usuario autenticado
    def get(self, request):
        experiencias = ExperienciaDisenoIngenieril.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Número de elementos por página
        resultado_paginado = paginator.paginate_queryset(experiencias, request)
        serializer = ExperienciaDisenoIngenierilSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST: Crear una nueva experiencia en diseño ingenieril
    def post(self, request):
        serializer = ExperienciaDisenoIngenierilSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({'mensaje': 'Experiencia en diseño ingenieril guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Actualizar una experiencia en diseño ingenieril existente
    def put(self, request, pk=None):
        experiencia = get_object_or_404(ExperienciaDisenoIngenieril, pk=pk, usuario=request.user)
        serializer = ExperienciaDisenoIngenierilSerializer(experiencia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Experiencia en diseño ingenieril actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Eliminar una experiencia en diseño ingenieril
    def delete(self, request, pk=None):
        experiencia = get_object_or_404(ExperienciaDisenoIngenieril, pk=pk, usuario=request.user)
        experiencia.delete()
        return Response({"mensaje": "Experiencia en diseño ingenieril eliminada correctamente."}, status=status.HTTP_200_OK)


