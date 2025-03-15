from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from productos_academicos.serializers import ProductosAcademicosRelevantesSerializer
from productos_academicos.models import ProductosAcademicosRelevantes
from institucion.views import InstitucionPais
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q


# Create your views here.

class ProductosAcademicosRelevantesView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: Listar todos los productos académicos del usuario autenticado
    def get(self, request):
        productos = ProductosAcademicosRelevantes.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Número de elementos por página
        resultado_paginado = paginator.paginate_queryset(productos, request)
        serializer = ProductosAcademicosRelevantesSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST: Crear un nuevo producto académico
    def post(self, request):
        serializer = ProductosAcademicosRelevantesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({'mensaje': 'Producto académico guardado correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Actualizar un producto académico existente
    def put(self, request, pk=None):
        producto = get_object_or_404(ProductosAcademicosRelevantes, pk=pk, usuario=request.user)
        serializer = ProductosAcademicosRelevantesSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Producto académico actualizado correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Eliminar un producto académico
    def delete(self, request, pk=None):
        producto = get_object_or_404(ProductosAcademicosRelevantes, pk=pk, usuario=request.user)
        producto.delete()
        return Response({"mensaje": "Producto académico eliminado correctamente."}, status=status.HTTP_200_OK)


