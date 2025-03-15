from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from experiencia_profesional.serializers import ExperienciaProfesionalNoAcademicaSerializer
from experiencia_profesional.models import ExperienciaProfesionalNoAcademica
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# Create your views here.

class ExperienciaProfesionalNoAcademicaView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: Listar todas las experiencias del usuario autenticado
    def get(self, request):
        experiencias = ExperienciaProfesionalNoAcademica.objects.filter(usuario=request.user).order_by('d_mes_anio')
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Número de elementos por página
        resultado_paginado = paginator.paginate_queryset(experiencias, request)
        serializer = ExperienciaProfesionalNoAcademicaSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST: Crear una nueva experiencia profesional
    def post(self, request):
        serializer = ExperienciaProfesionalNoAcademicaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({'mensaje': 'Experiencia profesional guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Actualizar una experiencia profesional existente
    def put(self, request, pk=None):
        experiencia = get_object_or_404(ExperienciaProfesionalNoAcademica, pk=pk, usuario=request.user)
        serializer = ExperienciaProfesionalNoAcademicaSerializer(experiencia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Experiencia profesional actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Eliminar una experiencia profesional
    def delete(self, request, pk=None):
        experiencia = get_object_or_404(ExperienciaProfesionalNoAcademica, pk=pk, usuario=request.user)
        experiencia.delete()
        return Response({"mensaje": "Experiencia profesional eliminada correctamente."}, status=status.HTTP_200_OK)
    
