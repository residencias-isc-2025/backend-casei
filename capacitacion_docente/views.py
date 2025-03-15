from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from capacitacion_docente.serializers import CapacitacionDocenteSerializer
from capacitacion_docente.models import CapacitacionDocente
from institucion.views import InstitucionPais
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q

class CapacitacionDocenteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        capacitaciones = CapacitacionDocente.objects.filter(usuario=request.user).order_by('anio_obtencion')
        result_page = paginator.paginate_queryset(capacitaciones, request)
        serializer = CapacitacionDocenteSerializer(result_page, many=True)      
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = CapacitacionDocenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({"mensaje": "Capacitación docente registrada correctamente.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de capacitacion."}, status=status.HTTP_400_BAD_REQUEST)
        
        capacitacion = get_object_or_404(CapacitacionDocente, pk=pk, usuario=request.user)
        serializer = CapacitacionDocenteSerializer(capacitacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Capacitación docente actualizada correctamente.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de capacitacion."}, status=status.HTTP_400_BAD_REQUEST)
        capacitacion = get_object_or_404(CapacitacionDocente, pk=pk, usuario=request.user)
        capacitacion.delete()
        return Response({"mensaje": "Capacitacion docente eliminada correctamente"}, status=status.HTTP_200_OK)



# Create your views here.
