from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from actividad.models import Actividad
from actividad.serializers import ActividadSerializer
from clase.models import Clase
from clase.serializers import ClaseSerializer
from django.shortcuts import get_object_or_404

class ActividadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        actividades = Actividad.objects.all().order_by('-id')
        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActividadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Actividad registrada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        actividad = get_object_or_404(Actividad, pk=pk)
        serializer = ActividadSerializer(actividad, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Actividad actualizada correctamente.', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        actividad = get_object_or_404(Actividad, pk=pk)
        actividad.delete()
        return Response({'mensaje': 'Actividad eliminada correctamente.'}, status=status.HTTP_200_OK)
    
class ActividadesPorClaseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clase_id):
        clase = get_object_or_404(Clase, pk=clase_id)
        actividades = Actividad.objects.filter(clase=clase).order_by('id')
        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
