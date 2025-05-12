from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from alumno.models import Alumno
from alumno.serializers import AlumnoSerializer
from django.shortcuts import get_object_or_404

class AlumnoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        alumnos = Alumno.objects.all()

        # Filtros
        matricula = request.query_params.get('matricula')
        if matricula:
            alumnos = alumnos.filter(matricula__icontains=matricula)

        nombre = request.query_params.get('nombre')
        if nombre:
            alumnos = alumnos.filter(nombre__icontains=nombre)

        apellido_materno = request.query_params.get('apellido_materno')
        if apellido_materno:
            alumnos = alumnos.filter(apellido_materno__icontains=apellido_materno)

        apellido_paterno = request.query_params.get('apellido_paterno')
        if apellido_paterno:
            alumnos = alumnos.filter(apellido_paterno__icontains=apellido_paterno)

        carrera = request.query_params.get('carrera')
        if carrera:
            alumnos = alumnos.filter(carrera_id=carrera)

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            if is_active.lower() in ['true', '1']:
                alumnos = alumnos.filter(is_active=True)
            elif is_active.lower() in ['false', '0']:
                alumnos = alumnos.filter(is_active=False)

        # Ordenar por matrícula
        alumnos = alumnos.order_by('matricula')

        # Paginación
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado = paginator.paginate_queryset(alumnos, request)
        serializer = AlumnoSerializer(resultado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = AlumnoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Alumno registrado correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)

        alumno = get_object_or_404(Alumno, pk=pk, is_active=True) 
        serializer = AlumnoSerializer(alumno, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Alumno actualizado correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere el ID.'}, status=status.HTTP_400_BAD_REQUEST)

        alumno = get_object_or_404(Alumno, pk=pk, is_active=True)
        alumno.is_active = False
        alumno.save()
        return Response({'mensaje': 'Alumno desactivado correctamente.'}, status=status.HTTP_200_OK)
    
class AlumnoCountView(APIView):
    def get(self, request):
        total = Alumno.objects.count()
        return Response({'total_alumnos': total}, status=status.HTTP_200_OK)

class HablitarAlumnoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'Se requiere un ID de alumno para habilitar'}, status=status.HTTP_400_BAD_REQUEST)
        
        alumno = get_object_or_404(Alumno, pk=pk)
        alumno.is_active = True
        alumno.save()
        return Response({'mensaje': 'Alumno activado correctamente'}, status=status.HTTP_200_OK)