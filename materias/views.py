from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from materias.models import Materia
from materias.serializers import MateriaSerializer
from django.shortcuts import get_object_or_404

class MateriaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            materia = get_object_or_404(Materia, pk=pk)
            serializer = MateriaSerializer(materia)
            return Response(serializer.data)
        
        materias = Materia.objects.all()
        # ✅ Filtros
        nombre = request.query_params.get('nombre')
        if nombre:
            materias = materias.filter(nombre__icontains=nombre)

        clave = request.query_params.get('clave')
        if clave:
            materias = materias.filter(clave__icontains=clave)

        semestre = request.query_params.get('semestre')
        if semestre:
            materias = materias.filter(semestre__icontains=semestre)

        tipo_curso = request.query_params.get('tipo_curso')
        if tipo_curso is not None:
            if tipo_curso.lower() in ['true', '1', 'obligatoria']:
                materias = materias.filter(tipo_curso=True)
            elif tipo_curso.lower() in ['false', '0', 'optativa']:
                materias = materias.filter(tipo_curso=False)

        materias = materias.order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(materias, request)
        serializer = MateriaSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = MateriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Materia registrada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        materia = get_object_or_404(Materia, pk=pk)
        serializer = MateriaSerializer(materia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Materia actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)
        materia = get_object_or_404(Materia, pk=pk)
        materia.delete()
        return Response({'mensaje': 'Materia eliminada correctamente.'}, status=status.HTTP_200_OK)
    