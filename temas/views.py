from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from temas.models import Temas
from temas.serializers import TemasSerializers
from django.shortcuts import get_object_or_404

class TemasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        temas = Temas.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(temas, request)
        serializer = TemasSerializers(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TemasSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Tema creado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de tema."}, status=status.HTTP_400_BAD_REQUEST)
        
        tema = get_object_or_404(Temas, pk=pk)
        serializer = TemasSerializers(tema, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Tema actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de tema."}, status=status.HTTP_400_BAD_REQUEST)
        
        tema = get_object_or_404(Temas, pk=pk)
        tema.delete()
        return Response({"mensaje": "Tema eliminado correctamente."}, status=status.HTTP_200_OK)
    
