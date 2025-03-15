from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from participacion.serializers import ParticipacionSerializer
from participacion.models import Participacion
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.

class ParticipacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todas las participaciones del usuario autenticado"""
        participaciones = Participacion.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(participaciones, request)
        serializer = ParticipacionSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea una nueva participación para el usuario autenticado"""
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = ParticipacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Participación guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza una participación existente"""
        participacion = get_object_or_404(Participacion, pk=pk, usuario=request.user)
        serializer = ParticipacionSerializer(participacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Participación actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina una participación existente"""
        participacion = get_object_or_404(Participacion, pk=pk, usuario=request.user)
        participacion.delete()
        return Response({'mensaje': 'Participación eliminada correctamente.'}, status=status.HTTP_200_OK)


