from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from criterio_desempeno.models import CriterioDesempeno
from criterio_desempeno.serializers import CriterioDesempenoSerializers
from django.shortcuts import render, get_object_or_404
# Create your views here.

class CriterioDesempenoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        criterios = CriterioDesempeno.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado = paginator.paginate_queryset(criterios, request)
        serializer = CriterioDesempenoSerializers(resultado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CriterioDesempenoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Criterio de desempeño creado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere el ID del criterio."}, status=status.HTTP_400_BAD_REQUEST)
        
        criterio = get_object_or_404(CriterioDesempeno, pk=pk)
        serializer = CriterioDesempenoSerializers(criterio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Criterio de desempeño actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere el ID del criterio."}, status=status.HTTP_400_BAD_REQUEST)
        
        criterio = get_object_or_404(CriterioDesempeno, pk=pk)
        criterio.delete()
        return Response({"mensaje": "Criterio de desempeño eliminado correctamente."}, status=status.HTTP_200_OK)
