from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from competencias_genericas.models import CompetenciaGenerica
from competencias_genericas.serializers import CompetenciaGenericaSerializer
from django.shortcuts import get_object_or_404

class CompetenciaGenericaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        competencias = CompetenciaGenerica.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(competencias, request)
        serializer = CompetenciaGenericaSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CompetenciaGenericaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Competencia registrada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        competencia = get_object_or_404(CompetenciaGenerica, pk=pk)
        serializer = CompetenciaGenericaSerializer(competencia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Competencia actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        competencia = get_object_or_404(CompetenciaGenerica, pk=pk)
        competencia.delete()
        return Response({'mensaje': 'Competencia eliminada correctamente.'}, status=status.HTTP_200_OK)