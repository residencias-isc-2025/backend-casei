from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from estrategia_evaluacion.serializers import EstrategiaEvaluacionSerializers
from estrategia_evaluacion.models import EstrategiaEvaluacion
from django.shortcuts import render, get_object_or_404

# Create your views here.
class EstrategiaEvaluacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        estrategia = EstrategiaEvaluacion.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(estrategia, request)
        serializer = EstrategiaEvaluacionSerializers(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea un nuevo objetivo específico."""
        serializer = EstrategiaEvaluacionSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Estrategia de evaluacion guardado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza un objetivo específico existente."""
        if not pk:
            return Response({"error": "Se requiere un ID de Estrategia de evaluacion."}, status=status.HTTP_400_BAD_REQUEST)

        estrategia = get_object_or_404(EstrategiaEvaluacion, pk=pk)
        serializer = EstrategiaEvaluacionSerializers(estrategia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Estrategia de evaluacion actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina un objetivo específico."""
        if not pk:
            return Response({"error": "Se requiere un ID de Estrategia de ensenanza."}, status=status.HTTP_400_BAD_REQUEST)

        objetivo = get_object_or_404(EstrategiaEvaluacion, pk=pk)
        objetivo.delete()
        return Response({"mensaje": "Estrategia de evaluacion eliminado correctamente."}, status=status.HTTP_200_OK)
