from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from objetivos_educacionales.models import ObjetivoEducacional
from objetivos_educacionales.serializers import ObjetivoEducacionalSerializer
from django.shortcuts import get_object_or_404

class ObjetivoEducacionalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        objetivos = ObjetivoEducacional.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(objetivos, request)
        serializer = ObjetivoEducacionalSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ObjetivoEducacionalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Objetivo educacional registrado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        objetivo = get_object_or_404(ObjetivoEducacional, pk=pk)
        serializer = ObjetivoEducacionalSerializer(objetivo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Objetivo educacional actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        objetivo = get_object_or_404(ObjetivoEducacional, pk=pk)
        objetivo.delete()
        return Response({'mensaje': 'Objetivo educacional eliminado correctamente.'}, status=status.HTTP_200_OK)