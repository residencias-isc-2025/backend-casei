from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from sub_temas.models import Subtema
from sub_temas.serializers import SubtemaSerializer
from django.shortcuts import get_object_or_404

class SubtemaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subtemas = Subtema.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(subtemas, request)
        serializer = SubtemaSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubtemaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Subtema registrado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        subtema = get_object_or_404(Subtema, pk=pk)
        serializer = SubtemaSerializer(subtema, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Subtema actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        subtema = get_object_or_404(Subtema, pk=pk)
        subtema.delete()
        return Response({'mensaje': 'Subtema eliminado correctamente.'}, status=status.HTTP_200_OK)