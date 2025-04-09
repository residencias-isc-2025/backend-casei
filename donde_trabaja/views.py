from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from donde_trabaja.models import DondeTrabaja
from donde_trabaja.serializers import DondeTrabajaSerializer
from django.shortcuts import get_object_or_404

class DondeTrabajaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lugares = DondeTrabaja.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(lugares, request)
        serializer = DondeTrabajaSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = DondeTrabajaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Lugar registrado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        lugar = get_object_or_404(DondeTrabaja, pk=pk)
        serializer = DondeTrabajaSerializer(lugar, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Lugar actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        lugar = get_object_or_404(DondeTrabaja, pk=pk)
        lugar.delete()
        return Response({'mensaje': 'Lugar eliminado correctamente.'}, status=status.HTTP_200_OK)