from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from gestion_academica.serializers import GestionAcademicaSerializer
from gestion_academica.models import GestionAcademica
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.

class GestionAcademicaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            gestion_academica = get_object_or_404(GestionAcademica, pk=pk, usuario=request.user)
            serializer = GestionAcademicaSerializer(gestion_academica)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        gestion_academica = GestionAcademica.objects.filter(usuario=request.user).order_by('d_mes_anio')
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Número de elementos por página
        resultado_paginado = paginator.paginate_queryset(gestion_academica, request)
        serializer = GestionAcademicaSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = GestionAcademicaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Gestión académica guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        gestion_academica = get_object_or_404(GestionAcademica, pk=pk, usuario=request.user)
        serializer = GestionAcademicaSerializer(gestion_academica, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Gestión académica actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        gestion_academica = get_object_or_404(GestionAcademica, pk=pk, usuario=request.user)
        gestion_academica.delete()
        return Response({'mensaje': 'Gestión académica eliminada correctamente.'}, status=status.HTTP_200_OK)


