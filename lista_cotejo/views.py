from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from lista_cotejo.models import ListaCotejo
from lista_cotejo.serializers import ListaCotejoSerializer
from django.shortcuts import get_object_or_404

class ListaCotejoView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        listas = ListaCotejo.objects.all().order_by('-id')
        serializer = ListaCotejoSerializer(listas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ListaCotejoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Lista de cotejo registrada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        lista = get_object_or_404(ListaCotejo, pk=pk)
        serializer = ListaCotejoSerializer(lista, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Lista actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        lista = get_object_or_404(ListaCotejo, pk=pk)
        lista.delete()
        return Response({'mensaje': 'Lista eliminada correctamente.'}, status=status.HTTP_200_OK)