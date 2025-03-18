from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from materia.models import Materia
from materia.serializers import MateriaSerializer

class MateriaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todas las materias con paginación."""
        materias = Materia.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(materias, request)
        serializer = MateriaSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea una nueva materia."""
        serializer = MateriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Materia creada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza una materia existente."""
        if not pk:
            return Response({"error": "Se requiere un ID de materia."}, status=status.HTTP_400_BAD_REQUEST)

        materia = get_object_or_404(Materia, pk=pk)
        serializer = MateriaSerializer(materia, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Materia actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina una materia."""
        if not pk:
            return Response({"error": "Se requiere un ID de materia."}, status=status.HTTP_400_BAD_REQUEST)

        materia = get_object_or_404(Materia, pk=pk)
        materia.delete()
        return Response({"mensaje": "Materia eliminada correctamente."}, status=status.HTTP_200_OK)