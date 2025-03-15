from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from formacion_academica.models import FormacionAcademica
from formacion_academica.serializers import FormacionAcademicaSerializer
from institucion.views import InstitucionPais
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# Create your views here.

class UserFormacionAcademicaView(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        formacion = FormacionAcademica.objects.filter(usuario=request.user).order_by('anio_obtencion')
        result_page = paginator.paginate_queryset(formacion, request)
        serializer = FormacionAcademicaSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        
        data = request.data.copy()  
        data["usuario"] = request.user.id

        serializer = FormacionAcademicaSerializer(data=data)
        if serializer.is_valid():
            serializer.save(usuario=request.user) 
            return Response(
                {"mensaje": "Formación académica registrada correctamente.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        
        formacion_id = request.data.get("id")

        try:
            formacion = FormacionAcademica.objects.get(id=formacion_id, usuario=request.user)
        except FormacionAcademica.DoesNotExist:
            return Response({"error": "No tienes permiso para modificar este registro."}, status=status.HTTP_403_FORBIDDEN)

        serializer = FormacionAcademicaSerializer(formacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Formación académica actualizada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de formación académica."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            formacion = FormacionAcademica.objects.get(id=pk, usuario=request.user)
            formacion.delete()
            return Response({"mensaje": "Formación académica eliminada correctamente."}, status=status.HTTP_200_OK)
        except FormacionAcademica.DoesNotExist:
            return Response({"error": "No tienes permiso para eliminar este registro o no existe."}, status=status.HTTP_403_FORBIDDEN)


