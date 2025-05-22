import csv
from datetime import date
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from atributo_egreso.models import AtributoEgreso
from atributo_egreso.serializers import AtributoEgresoSerializers
from bibliografia.models import Bibliografia
from bibliografia.serializers import BibliografiaSerializers
from clase.serializers import ClaseSerializer
from competencia.models import Competencia
from competencia.serializers import CompetenciaSerializer
from criterio_desempeno.models import CriterioDesempeno
from criterio_desempeno.serializers import CriterioDesempenoSerializers
from estrategia_ensenanza.models import EstrategiaEnsenanza
from estrategia_ensenanza.serializers import EstrategiaEnsenanzaSerializers
from estrategia_evaluacion.models import EstrategiaEvaluacion
from estrategia_evaluacion.serializers import EstrategiaEvaluacionSerializers
from materias.models import Materia
from materias.serializers import MateriaSerializer
from objetivos_especificos.models import ObjetivosEspecificos
from objetivos_especificos.serializers import ObjetivosEspecificosSerializers
from practica.models import Practica
from practica.serializers import PracticaSerializers
from temas.models import Temas
from temas.serializers import TemasSerializers
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
from django.utils.timezone import now
from clase.models import Clase
from periodo.models import Periodo
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

class ProgramaAsignaturaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            materia = get_object_or_404(Materia, pk=pk)
            materia_data = MateriaSerializer(materia).data

            hoy = date.today()
            periodo_actual = Periodo.objects.filter(fecha_inicio__lte=hoy, fecha_fin__gte=hoy).first()
            total_clases = 0
            docentes = []

            if periodo_actual:
                clases = Clase.objects.filter(periodo=periodo_actual, materia=materia)
                total_clases = clases.count()
                
                clases_qs = Clase.objects.filter(
                    periodo=periodo_actual,
                    materia=materia,
                    docente__isnull=False
                ).select_related('docente').distinct()
                
                clases_serialized = ClaseSerializer(clases, many=True).data
                
                NIVEL_JERARQUIA = {'L': 1, 'E': 2, 'M': 3, 'D': 4}

                docentes_ids = clases_qs.values_list('docente__id', flat=True).distinct()
                for docente_id in docentes_ids:
                    docente = CustomUser.objects.get(id=docente_id)
                    formaciones = FormacionAcademica.objects.filter(usuario=docente)

                    nivel_mas_alto = None
                    for f in formaciones:
                        nivel = f.nivel
                        if nivel and (not nivel_mas_alto or NIVEL_JERARQUIA.get(nivel, 0) > NIVEL_JERARQUIA.get(nivel_mas_alto, 0)):
                            nivel_mas_alto = nivel

                    docentes.append({
                        "id": docente.id,
                        "username": docente.username,
                        "apellido_materno": docente.apellido_materno,
                        "apellido_paterno": docente.apellido_paterno,
                        "nombre": docente.nombre,
                        "grado_academico": nivel_mas_alto
                    })

            # Resto del código para serializar la materia
            competencias_ids = materia_data.get('competencias', [])
            criterios_desempenio_ids = materia_data.get('criterio_desempeno', [])
            bibliografias_ids = materia_data.get('bibliografia', [])
            competencias_qs = Competencia.objects.filter(id__in=competencias_ids)
            competencias_data = CompetenciaSerializer(competencias_qs, many=True).data

            objetivos_especificos_ids = set()
            temas_ids = set()
            atributos_egreso_ids = set()
            estrategias_ensenanza_ids = set()
            estrategias_evaluacion_ids = set()
            practicas_ids = set()

            for competencia in competencias_data:
                if competencia.get('objetivos_especificos'):
                    objetivos_especificos_ids.add(competencia['objetivos_especificos'])
                if competencia.get('temas'):
                    temas_ids.update(competencia['temas'])

            objetivos_qs = ObjetivosEspecificos.objects.filter(id__in=objetivos_especificos_ids)
            objetivos_data = ObjetivosEspecificosSerializers(objetivos_qs, many=True).data

            temas_qs = Temas.objects.filter(id__in=temas_ids)
            temas_data = TemasSerializers(temas_qs, many=True).data

            for tema in temas_data:
                if tema.get('estrategia_ensenanza'):
                    estrategias_ensenanza_ids.add(tema['estrategia_ensenanza'])
                if tema.get('estrategia_evaluacion'):
                    estrategias_evaluacion_ids.add(tema['estrategia_evaluacion'])
                if tema.get('practica'):
                    practicas_ids.add(tema['practica'])

            criterios_desempeno_qs = CriterioDesempeno.objects.filter(id__in=criterios_desempenio_ids)
            criterios_desempenio_data = CriterioDesempenoSerializers(criterios_desempeno_qs, many=True).data

            for criterio in criterios_desempenio_data:
                if criterio.get('atributo_egreso'):
                    atributos_egreso_ids.add(criterio['atributo_egreso'])

            atributos_egreso_qs = AtributoEgreso.objects.filter(id__in=atributos_egreso_ids)
            atributos_egreso_data = AtributoEgresoSerializers(atributos_egreso_qs, many=True).data

            estrategias_ensenanza_qs = EstrategiaEnsenanza.objects.filter(id__in=estrategias_ensenanza_ids)
            estrategias_ensenanza_data = EstrategiaEnsenanzaSerializers(estrategias_ensenanza_qs, many=True).data

            estrategias_evaluacion_qs = EstrategiaEvaluacion.objects.filter(id__in=estrategias_evaluacion_ids)
            estrategias_evaluacion_data = EstrategiaEvaluacionSerializers(estrategias_evaluacion_qs, many=True).data

            practicas_qs = Practica.objects.filter(id__in=practicas_ids)
            practicas_data = PracticaSerializers(practicas_qs, many=True).data

            bibliografias_qs = Bibliografia.objects.filter(id__in=bibliografias_ids)
            bibliografias_data = BibliografiaSerializers(bibliografias_qs, many=True).data

            data = {
                "materia": materia_data,
                "competencias": competencias_data,
                "objetivos_especificos": objetivos_data,
                "temas": temas_data,
                "atributos_egreso": atributos_egreso_data,
                "estrategias_ensenanza": estrategias_ensenanza_data,
                "estrategias_evaluacion": estrategias_evaluacion_data,
                "practicas": practicas_data,
                "bibliografias": bibliografias_data,
                "total_clases_periodo_actual": total_clases,
                "docentes_periodo_actual": docentes,
                "clases": clases_serialized
            }

            return Response(data, status=status.HTTP_200_OK)
        

