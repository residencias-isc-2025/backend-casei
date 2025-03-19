from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from carrera.models import Carrera
from carrera.serializers import CarreraSerializer

class CarreraView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carreras = Carrera.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(carreras, request)
        serializer = CarreraSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CarreraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Carrera creada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de carrera."}, status=status.HTTP_400_BAD_REQUEST)

        carrera = get_object_or_404(Carrera, pk=pk)
        serializer = CarreraSerializer(carrera, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Carrera actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de carrera."}, status=status.HTTP_400_BAD_REQUEST)

        carrera = get_object_or_404(Carrera, pk=pk)
        carrera.delete()
        return Response({"mensaje": "Carrera eliminada correctamente."}, status=status.HTTP_200_OK)