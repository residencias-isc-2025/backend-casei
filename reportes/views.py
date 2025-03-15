import csv
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from usuarios.serializers import UserSerializer
from usuarios.models import CustomUser
from formacion_academica.serializers import FormacionAcademicaSerializer
from formacion_academica.models import FormacionAcademica
from actualizacion_diciplinar.serializers import ActualizacionDisciplinarSerializer
from actualizacion_diciplinar.models import ActualizacionDisciplinaria
from adscripcion.serializers import AreaAdscripcionSerializer
from adscripcion.models import AreaAdscripcion
from aportaciones.serializers import AportacionSerializer
from aportaciones.models import Aportacion
from capacitacion_docente.serializers import CapacitacionDocenteSerializer
from capacitacion_docente.models import CapacitacionDocente
from experiencia_diseno.serializers import ExperienciaDisenoIngenierilSerializer
from experiencia_diseno.models import ExperienciaDisenoIngenieril
from formacion_academica.serializers import FormacionAcademicaSerializer
from formacion_academica.models import FormacionAcademica
from experiencia_profesional.serializers import ExperienciaProfesionalNoAcademicaSerializer
from experiencia_profesional.models import ExperienciaProfesionalNoAcademica
from gestion_academica.serializers import GestionAcademicaSerializer
from gestion_academica.models import GestionAcademica
from institucion.serializers import InstitucionPaisSerializer
from institucion.models import InstitucionPais
from logros_profesionales.serializers import LogrosProfesionalesSerializer
from logros_profesionales.models import LogrosProfesionales
from participacion.serializers import ParticipacionSerializer
from participacion.models import Participacion
from premios.serializers import PremioSerializer
from premios.models import Premio
from productos_academicos.serializers import ProductosAcademicosRelevantesSerializer
from productos_academicos.models import ProductosAcademicosRelevantes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.

def es_admin_o_superusuario(user):
    return user.is_staff or user.is_superuser

#Endpoint GET TODAS LAS TABLAS
class CurriculumVitaeView(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        """Devuelve todos los datos de todas las tablas registradas"""
        usuario = request.user

        data = {
            "usuario": UserSerializer(usuario).data,
            "formacion_academica": FormacionAcademicaSerializer(
                FormacionAcademica.objects.filter(usuario=usuario).order_by('-anio_obtencion'), many=True
            ).data,
            "capacitacion_docente": CapacitacionDocenteSerializer(
                CapacitacionDocente.objects.filter(usuario=usuario).order_by('-anio_obtencion'), many=True
            ).data,
            "actualizacion_disciplinaria": ActualizacionDisciplinarSerializer(
                ActualizacionDisciplinaria.objects.filter(usuario=usuario).order_by('-anio_obtencion'), many=True
            ).data,
            "gestion_academica": GestionAcademicaSerializer(
                GestionAcademica.objects.filter(usuario=usuario).order_by('-a_mes_anio'), many=True
            ).data,
            "productos_academicos_relevantes": ProductosAcademicosRelevantesSerializer(
                ProductosAcademicosRelevantes.objects.filter(usuario=usuario).order_by('-id'), many=True
            ).data,
            "experiencia_no_academica": ExperienciaProfesionalNoAcademicaSerializer(
                ExperienciaProfesionalNoAcademica.objects.filter(usuario=usuario).order_by('-a_mes_anio'), many=True
            ).data,
            "experiencia_diseno_ingenieril": ExperienciaDisenoIngenierilSerializer(
                ExperienciaDisenoIngenieril.objects.filter(usuario=usuario).order_by('-periodo'), many=True
            ).data,
            "logros_profesionales": LogrosProfesionalesSerializer(
                LogrosProfesionales.objects.filter(usuario=usuario).order_by('-id'), many=True
            ).data,
            "participacion": ParticipacionSerializer(
                Participacion.objects.filter(usuario=usuario).order_by('-periodo'), many=True
            ).data,
            "premios": PremioSerializer(
                Premio.objects.filter(usuario=usuario).order_by('-id'), many=True
            ).data,
            "aportaciones": AportacionSerializer(
                Aportacion.objects.filter(usuario=usuario).order_by('-id'), many=True
            ).data,
        }

        return Response(data, status=status.HTTP_200_OK)
    
#Endpoint Crear usuarios usando un archivo CSV
class CreateUsersByCsvView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        archivo_csv = request.FILES.get('archivo_csv')

        if not archivo_csv:
            return Response({"error": "No se proporcionó ningún archivo CSV."}, status=status.HTTP_400_BAD_REQUEST)
        if not es_admin_o_superusuario(request.user):
            return Response({"error": "No tienes permisos para cargar archivos CSV."}, status=status.HTTP_403_FORBIDDEN)
        try:
            # Leer el archivo CSV y registrar usuarios
            csv_reader = csv.DictReader(archivo_csv.read().decode('utf-8').splitlines())
            usuarios_creados = []
            errores = []

            for fila in csv_reader:
                try:
                    # Extraer datos del CSV
                    username = fila.get('username')
                    role = fila.get('role')
                    tipo_docente = fila.get('tipo_docente', None) if role == 'user' else None
                    apellido_materno = fila.get('apellido_materno', "")
                    apellido_paterno = fila.get('apellido_paterno', "")
                    nombre = fila.get('nombre', "")
                    fecha_nacimiento = fila.get('fecha_nacimiento', None)

                    # Validar campos obligatorios
                    if not username or not role:
                        errores.append(f"Faltan datos obligatorios en la fila: {fila}")
                        continue

                    if role not in ['superuser', 'admin', 'user']:
                        errores.append(f"Rol inválido para el usuario '{username}'.")
                        continue

                    # Validar tipo_docente solo si el usuario es docente
                    if role == 'user' and tipo_docente not in ['basificado', 'asignatura']:
                        errores.append(f"El 'tipo_docente' debe ser 'basificado' o 'asignatura' para el usuario '{username}'.")
                        continue

                    # Verificar si el Usuario ya existe
                    if CustomUser.objects.filter(username=username).exists():
                        errores.append(f"El nombre de usuario '{username}' ya está registrado.")
                        continue

                    # Crear el usuario
                    user = CustomUser.objects.create(
                        username=username,
                        password=make_password(username),  # La contraseña será el mismo username
                        role=role,
                        tipo_docente=tipo_docente,
                        apellido_materno=apellido_materno,
                        apellido_paterno=apellido_paterno,
                        nombre=nombre,
                        fecha_nacimiento=fecha_nacimiento,
                        is_staff=(role in ['admin', 'superuser']),
                        is_superuser=(role == 'superuser')
                    )
                    usuarios_creados.append(username)

                except Exception as e:
                    errores.append(f"Error al crear el usuario con los datos: {fila}. Error: {str(e)}")

            resultado = {
                "usuarios_creados": usuarios_creados,
                "errores": errores
            }

            return Response({
                "mensaje": f"Se procesaron {len(usuarios_creados)} usuarios.",
                "resultado": resultado
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error al procesar el archivo CSV: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
