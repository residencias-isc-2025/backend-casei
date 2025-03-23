from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from bibliografia.models import Bibliografia
from bibliografia.serializers import BibliografiaSerializers
from django.shortcuts import render, get_object_or_404

class BibliografiaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bibliografia = Bibliografia.objects.all().order_by('-anio')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(bibliografia, request)
        serializer = BibliografiaSerializers(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = BibliografiaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Bibliografía registrada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID de la bibliografía.'}, status=status.HTTP_400_BAD_REQUEST)

        bib = get_object_or_404(Bibliografia, pk=pk)
        serializer = BibliografiaSerializers(bib, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Bibliografía actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID de la bibliografía.'}, status=status.HTTP_400_BAD_REQUEST)

        bib = get_object_or_404(Bibliografia, pk=pk)
        bib.delete()
        return Response({'mensaje': 'Bibliografía eliminada correctamente.'}, status=status.HTTP_200_OK)