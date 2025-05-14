from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from institucion.models import InstitucionPais
from institucion.serializers import InstitucionPaisSerializer
import csv


# Create your views here.
class InstitucionPaisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Devuelve la lista de todas las instituciones o una en específico si se pasa un ID."""
        paginator = PageNumberPagination()
        
        # Permitir que el usuario defina el tamaño de la página desde los parámetros de consulta
        page_size = request.query_params.get('page_size', 10)  # Valor predeterminado de 10
        try:
            paginator.page_size = int(page_size)
        except ValueError:
            paginator.page_size = 10  # Valor predeterminado si el parámetro no es un número válido

        if pk:
            institucion = get_object_or_404(InstitucionPais, pk=pk)
            serializer = InstitucionPaisSerializer(institucion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Construir el queryset con filtros dinámicos
        instituciones = InstitucionPais.objects.all().order_by('nombre_institucion')

        # Obtener parámetros de búsqueda desde la URL
        search_institucion = request.query_params.get('institucion', None)
        search_pais = request.query_params.get('pais', None)
        search_estado = request.query_params.get('estado', None)

        # Aplicar filtros condicionales
        if search_institucion:
            instituciones = instituciones.filter(nombre_institucion__icontains=search_institucion)
        if search_pais:
            instituciones = instituciones.filter(pais__iexact=search_pais)
        if search_estado:
            instituciones = instituciones.filter(estado__iexact=search_estado)

        # Aplicar paginación al queryset filtrado
        result_page = paginator.paginate_queryset(instituciones, request)
        serializer = InstitucionPaisSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Permite registrar una nueva institución y país."""
        serializer = InstitucionPaisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Institución registrada correctamente.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Permite actualizar los datos de una institución."""
        if not pk:
            return Response({"error": "Se requiere un ID para actualizar una institución."}, status=status.HTTP_400_BAD_REQUEST)
        institucion = get_object_or_404(InstitucionPais, pk=pk)
        serializer = InstitucionPaisSerializer(institucion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Institución actualizada correctamente.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Inhabilita (marca como inactiva) una institución en lugar de eliminarla."""
        if not pk:
            return Response({"error": "Se requiere un ID para inhabilitar una institución."}, status=status.HTTP_400_BAD_REQUEST)

        institucion = get_object_or_404(InstitucionPais, pk=pk)

        institucion.estado = 'inactivo'
        institucion.save()

        return Response({"mensaje": "Institución marcada como inactiva correctamente."}, status=status.HTTP_200_OK)

class HabilitarInstitucionView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        """Habilita una institución previamente marcada como inactiva."""
        if not pk:
            return Response({"error": "Se requiere un ID de institución para habilitarla."}, status=status.HTTP_400_BAD_REQUEST)

        institucion = get_object_or_404(InstitucionPais, pk=pk)

        if institucion.estado == 'activo':
            return Response({"mensaje": f"La institución {institucion.nombre_institucion} ya está activa."}, status=status.HTTP_400_BAD_REQUEST)

        institucion.estado = 'activo'
        institucion.save()

        return Response({"mensaje": f"Institución {institucion.nombre_institucion} habilitada correctamente."}, status=status.HTTP_200_OK)

class InstitucionByCsvView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        archivo_csv = request.FILES.get('archivo_csv')
        
        if not archivo_csv:
            return Response({"error": "No se proporcionó ningún archivo CSV."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            csv_reader = csv.DictReader(archivo_csv.read().decode('utf-8').splitlines())
            instituciones = []
            errores = []
            
            for adscripcion in csv_reader:
                try:
                    nombre_institucion = adscripcion.get('nombre')
                    pais = adscripcion.get('pais')
                    
                    if not nombre_institucion or not pais:
                        errores.append(f"Faltan datos obligatorios en la fila: {adscripcion}")
                        continue
                    
                    institucion_pais = InstitucionPais.objects.create(
                        nombre_institucion=nombre_institucion,
                        pais=pais
                    )
                    
                    instituciones.append(nombre_institucion)
                    
                except Exception as e:
                    errores.append(f"Error al crear instituciones con los datos: {adscripcion}. Error: {str(e)}")
            
            resultado = {
                "instituciones_creadas": instituciones,
                "errores": errores
            }
            
            return Response({
                "mensaje": f"Se procesaron {len(instituciones)} instituciones.",
                "resultado": resultado
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": f"Error al procesar el archivo CSV: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
            