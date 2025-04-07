from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from nivel_desempenio.models import NivelDesempenio
from nivel_desempenio.serializers import NivelDesempenioSerializer
from django.shortcuts import get_object_or_404

class NivelDesempenioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        niveles = NivelDesempenio.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(niveles, request)
        serializer = NivelDesempenioSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = NivelDesempenioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Nivel registrado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        nivel = get_object_or_404(NivelDesempenio, pk=pk)
        serializer = NivelDesempenioSerializer(nivel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Nivel actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        nivel = get_object_or_404(NivelDesempenio, pk=pk)
        nivel.delete()
        return Response({'mensaje': 'Nivel eliminado correctamente.'}, status=status.HTTP_200_OK)