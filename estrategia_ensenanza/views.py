from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from estrategia_ensenanza.serializers import EstrategiaEnsenanzaSerializers
from estrategia_ensenanza.models import EstrategiaEnsenanza
from django.shortcuts import render, get_object_or_404

# Create your views here.
class EstrategiaEnsenanzaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        estrategia = EstrategiaEnsenanza.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(estrategia, request)
        serializer = EstrategiaEnsenanzaSerializers(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea un nuevo objetivo específico."""
        serializer = EstrategiaEnsenanzaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Estrategia de ensenanza guardado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza un objetivo específico existente."""
        if not pk:
            return Response({"error": "Se requiere un ID de Estrategia de ensenanza."}, status=status.HTTP_400_BAD_REQUEST)

        estrategia = get_object_or_404(EstrategiaEnsenanza, pk=pk)
        serializer = EstrategiaEnsenanzaSerializers(estrategia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Estrategia de ensenanza actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina un objetivo específico."""
        if not pk:
            return Response({"error": "Se requiere un ID de Estrategia de ensenanza."}, status=status.HTTP_400_BAD_REQUEST)

        objetivo = get_object_or_404(EstrategiaEnsenanza, pk=pk)
        objetivo.delete()
        return Response({"mensaje": "Estrategia de ensenanza eliminado correctamente."}, status=status.HTTP_200_OK)
