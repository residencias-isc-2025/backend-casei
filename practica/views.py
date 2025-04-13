from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from practica.serializers import PracticaSerializers
from practica.models import Practica
from django.shortcuts import render, get_object_or_404

# Create your views here.
class PracticaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        practicas = Practica.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(practicas, request)
        serializer = PracticaSerializers(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PracticaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Práctica creada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de práctica."}, status=status.HTTP_400_BAD_REQUEST)

        practica = get_object_or_404(Practica, pk=pk)
        serializer = PracticaSerializers(practica, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Práctica actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de práctica."}, status=status.HTTP_400_BAD_REQUEST)

        practica = get_object_or_404(Practica, pk=pk)
        practica.delete()
        return Response({"mensaje": "Práctica eliminada correctamente."}, status=status.HTTP_200_OK)
