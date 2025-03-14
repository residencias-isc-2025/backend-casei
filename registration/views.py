import csv
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from registration.serializers import FormacionAcademicaSerializer, ActualizacionDisciplinarSerializer, GestionAcademicaSerializer, ProductosAcademicosRelevantesSerializer, ExperienciaProfesionalNoAcademicaSerializer, ExperienciaDisenoIngenierilSerializer, LogrosProfesionalesSerializer, ParticipacionSerializer, PremioSerializer, AportacionSerializer
from registration.models import CustomUser, ActualizacionDisciplinaria, GestionAcademica, ProductosAcademicosRelevantes, ExperienciaProfesionalNoAcademica, ExperienciaDisenoIngenieril, LogrosProfesionales, Participacion, Premio, Aportacion
from usuarios.serializers import UserSerializer
from institucion.views import InstitucionPais
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q


def es_admin_o_superusuario(user):
    return user.is_staff or user.is_superuser

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10

# Enpoint De Registro
class RegisterUserView(APIView):
    permission_classes = [IsAuthenticated]  # 🔹 Solo usuarios autenticados pueden acceder

    def post(self, request):
        """Permite a Administradores y Super Usuarios crear cualquier tipo de usuario"""
        data = request.data

        # Verificar si el usuario que hace la solicitud es admin o superusuario
        if not request.user.is_staff:
            return Response({"mensaje": "No tienes permisos para crear usuarios."}, status=status.HTTP_403_FORBIDDEN)

        # Validar campos obligatorios generales
        required_fields = ['username', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return Response({"mensaje": f"El campo '{field}' es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)

        username = data.get('username')
        password = make_password(data.get('password'))  # Hashear la contraseña
        role = data.get('role')

        # Validar que el rol sea válido
        if role not in ['superuser', 'admin', 'user']:
            return Response({"mensaje": "Rol inválido. Debe ser 'superuser', 'admin' o 'user'."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Si el rol es 'user' (Docente), el campo tipo_docente es obligatorio
        tipo_docente = data.get('tipo_docente', None)
        if role == 'user' and not tipo_docente:
            return Response({"error": "El campo 'tipo_docente' es obligatorio para el rol 'user' (Docente)."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validar tipo_docente solo si el usuario es docente
        if role == 'user' and tipo_docente not in ['basificado', 'asignatura']:
            return Response({"error": "El 'tipo_docente' debe ser 'basificado' o 'asignatura'."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validar si el Usuario ya existe
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "El nombre de usuario ya está registrado. Elige otro."}, status=status.HTTP_400_BAD_REQUEST)

        # Campos opcionales
        apellido_materno = data.get('apellido_materno', "")
        apellido_paterno = data.get('apellido_paterno', "")
        nombre = data.get('nombre', "")
        fecha_nacimiento = data.get('fecha_nacimiento', None)
        area_adscripcion_id = data.get('area_adscripcion', None)  # ID del área de adscripción (opcional)

        # Validar que el área de adscripción exista si se proporciona
        area_adscripcion = None
        if area_adscripcion_id:
            try:
                area_adscripcion = AreaAdscripcion.objects.get(id=area_adscripcion_id)
            except AreaAdscripcion.DoesNotExist:
                return Response({"error": "El área de adscripción proporcionada no es válida."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.create(
                username=username,
                password=password,
                role=role,
                apellido_materno=apellido_materno,
                apellido_paterno=apellido_paterno,
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                area_adscripcion=area_adscripcion
            )

            # Asignar permisos según el rol
            if role == 'superuser':
                user.is_staff = True
                user.is_superuser = True
            elif role == 'admin':
                user.is_staff = True
                user.is_superuser = False
            else:  # Docente
                user.is_staff = False
                user.is_superuser = False
                user.tipo_docente = tipo_docente

            user.save()

            return Response({"mensaje": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        """Permite actualizar la información de un usuario (admin, superuser o el mismo usuario docente)"""
        if not pk:
            return Response({"error": "Se requiere un ID de usuario."}, status=status.HTTP_400_BAD_REQUEST)

        usuario = get_object_or_404(CustomUser, pk=pk)

        # Permitir solo si es admin, superuser o el mismo usuario autenticado si es tipo 'user'
        if not (request.user.is_staff or request.user == usuario):
            return Response({"error": "No tienes permisos para modificar este usuario."},
                            status=status.HTTP_403_FORBIDDEN)

        data = request.data

        # Validar si el nombre de usuario ya existe
        if "username" in data and data["username"] != usuario.username and CustomUser.objects.filter(username=data["username"]).exists():
            return Response({"error": "El nombre de usuario ya está registrado. Elige otro."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar el área de adscripción si se proporciona
        area_adscripcion_id = data.get('area_adscripcion', None)
        if area_adscripcion_id:
            try:
                area_adscripcion = AreaAdscripcion.objects.get(id=area_adscripcion_id)
                data['area_adscripcion'] = area_adscripcion.id
            except AreaAdscripcion.DoesNotExist:
                return Response({"error": "El área de adscripción proporcionada no es válida."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(usuario, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario actualizado correctamente", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Inhabilita (marca como inactivo) a un usuario en lugar de eliminarlo"""
        if not pk:
            return Response({"error": "Se requiere un ID de usuario."}, status=status.HTTP_400_BAD_REQUEST)

        usuario = get_object_or_404(CustomUser, pk=pk)

        if not request.user.is_staff:
            return Response({"error": "No tienes permisos para inhabilitar usuarios."}, status=status.HTTP_403_FORBIDDEN)

        usuario.estado = 'inactivo'
        usuario.save()

        return Response({"mensaje": f"Usuario {usuario.username} marcado como inactivo correctamente."}, status=status.HTTP_200_OK)

#Endpoint para Habilitar a un usuario Deshabilitado
class HabilitarUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        """Habilita un usuario previamente inhabilitado (marca como activo)"""
        if not pk:
            return Response({"error": "Se requiere un ID de usuario."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_staff:
            return Response({"error": "No tienes permisos para habilitar usuarios."}, status=status.HTTP_403_FORBIDDEN)

        usuario = get_object_or_404(CustomUser, pk=pk)

        if usuario.estado == 'activo':
            return Response({"mensaje": f"El usuario {usuario.username} ya está activo."}, status=status.HTTP_400_BAD_REQUEST)

        usuario.estado = 'activo'
        usuario.save()

        return Response({"mensaje": f"Usuario {usuario.username} habilitado correctamente."}, status=status.HTTP_200_OK)

# Enpoint de Token de Autorizacion
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """Devuelve el token de autenticación para un usuario"""
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user.id, 'username': token.user.username})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Por ejemplo, 'admin' o 'user'
        # Aquí podrías agregar validaciones adicionales
        try:
            user = CustomUser.objects.create_user(username=username, password=password, role=role)
            return redirect('login')
        except Exception as e:
            # Manejo de error, por ejemplo, mostrar un mensaje en el template
            return render(request, 'register.html', {'error': str(e)})
    return render(request, 'registration/register.html')


# Cabiar la Cotraseña del usuario
class ChangePasswordView(APIView):
    """Permite que cualquier usuario autenticado cambie su contraseña"""
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """Actualiza la contraseña del usuario autenticado sin confirmación de contraseña"""
        usuario = request.user
        new_password = request.data.get("new_password")

        if not new_password:
            return Response({"error": "El campo 'new_password' es obligatorio."},
                            status=status.HTTP_400_BAD_REQUEST)

        usuario.password = make_password(new_password)
        usuario.save()

        return Response({"mensaje": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)

#Endpoint de reseteo de contraseña
class ResetPasswordView(APIView):
    """
    Permite a Administradores y Super Usuarios resetear la contraseña de un docente.
    La nueva contraseña será igual al username del usuario.
    """
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def post(self, request, pk=None):
        """
        Permite que el admin o el superusuario reseteen la contraseña de otros usuarios.
        """
        if not pk:
            return Response({"error": "Se requiere un ID de usuario."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar si el usuario tiene permisos (admin o superusuario)
        if not es_admin_o_superusuario(request.user):
            return Response({"error": "No tienes permisos para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)

        usuario = get_object_or_404(CustomUser, pk=pk)
        
        # La nueva contraseña será el nombre de usuario
        nueva_contraseña = usuario.username
        usuario.password = make_password(nueva_contraseña)
        usuario.save()

        return Response({"mensaje": f"Contraseña restablecida correctamente."},
                        status=status.HTTP_200_OK)
        
# Endpoint de listado
class ListUsersView(ListAPIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    serializer_class = UserSerializer

    def get_queryset(self):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = CustomUser.objects.exclude(id=self.request.user.id).order_by('username')

        # Obtener parámetros de búsqueda desde la URL
        search_username = self.request.query_params.get('username', None)
        search_name = self.request.query_params.get('nombre', None)
        search_area_adscripcion = self.request.query_params.get('area_adscripcion', None)
        search_estado = self.request.query_params.get('estado', None)


        # Aplicar filtros condicionalmente
        if search_username:
            queryset = queryset.filter(username__startswith=search_username)
        if search_name:
            queryset = queryset.filter(nombre__startswith=search_name)
        if search_area_adscripcion:
            try:
                # Intentar convertir el ID del área de adscripción a un número entero
                area_adscripcion_id = int(search_area_adscripcion)
                queryset = queryset.filter(area_adscripcion__id=area_adscripcion_id)
            except ValueError:
                pass
        if search_estado:
            queryset = queryset.filter(estado__exact=search_estado)
        result_page = paginator.paginate_queryset(queryset, self.request)
        return result_page
    
# Endpoint de jalar la informacion del usuario autenticado
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Endpoint para la Formacion Academica
class UserFormacionAcademicaView(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        formacion = FormacionAcademica.objects.filter(usuario=request.user).order_by('anio_obtencion')
        result_page = paginator.paginate_queryset(formacion, request)
        serializer = FormacionAcademicaSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        
        data = request.data.copy()  
        data["usuario"] = request.user.id

        serializer = FormacionAcademicaSerializer(data=data)
        if serializer.is_valid():
            serializer.save(usuario=request.user) 
            return Response(
                {"mensaje": "Formación académica registrada correctamente.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        
        formacion_id = request.data.get("id")

        try:
            formacion = FormacionAcademica.objects.get(id=formacion_id, usuario=request.user)
        except FormacionAcademica.DoesNotExist:
            return Response({"error": "No tienes permiso para modificar este registro."}, status=status.HTTP_403_FORBIDDEN)

        serializer = FormacionAcademicaSerializer(formacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Formación académica actualizada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de formación académica."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            formacion = FormacionAcademica.objects.get(id=pk, usuario=request.user)
            formacion.delete()
            return Response({"mensaje": "Formación académica eliminada correctamente."}, status=status.HTTP_200_OK)
        except FormacionAcademica.DoesNotExist:
            return Response({"error": "No tienes permiso para eliminar este registro o no existe."}, status=status.HTTP_403_FORBIDDEN)
    
# EndPoint para la Institucion y Pais
"""
class InstitucionPaisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
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
        serializer = InstitucionPaisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Institución registrada correctamente.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID para actualizar una institución."}, status=status.HTTP_400_BAD_REQUEST)
        institucion = get_object_or_404(InstitucionPais, pk=pk)
        serializer = InstitucionPaisSerializer(institucion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Institución actualizada correctamente.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID para inhabilitar una institución."}, status=status.HTTP_400_BAD_REQUEST)

        institucion = get_object_or_404(InstitucionPais, pk=pk)

        institucion.estado = 'inactivo'
        institucion.save()

        return Response({"mensaje": "Institución marcada como inactiva correctamente."}, status=status.HTTP_200_OK)
"""
#Endpoint para Habilitar una institucion
"""
class HabilitarInstitucionView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        
        if not pk:
            return Response({"error": "Se requiere un ID de institución para habilitarla."}, status=status.HTTP_400_BAD_REQUEST)

        institucion = get_object_or_404(InstitucionPais, pk=pk)

        if institucion.estado == 'activo':
            return Response({"mensaje": f"La institución {institucion.nombre_institucion} ya está activa."}, status=status.HTTP_400_BAD_REQUEST)

        institucion.estado = 'activo'
        institucion.save()

        return Response({"mensaje": f"Institución {institucion.nombre_institucion} habilitada correctamente."}, status=status.HTTP_200_OK)

"""
@login_required
def dashboard(request):
    if request.user.role == "admin":
        mensaje = "Bienvenido, Administrador"
        return render(request, 'admin_dashboard.html', {'mensaje': mensaje})
    elif request.user.role == "user":
        mensaje = "Bienvenido, Docente"
        return render(request, 'user_dashboard.html', {'mensaje': mensaje})
    elif request.user.role == "superuser":
        mensaje = "Bienvenido, Super Usuario"
        return render(request, 'user_dashboard.html', {'mensaje': mensaje})
    else:
        mensaje = "Bienvenido, Usuario"
        return render(request, 'dashboard.html', {'mensaje': mensaje})

#Endpoint Capacitacion Docente
class CapacitacionDocenteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        capacitaciones = CapacitacionDocente.objects.filter(usuario=request.user).order_by('anio_obtencion')
        result_page = paginator.paginate_queryset(capacitaciones, request)
        serializer = CapacitacionDocenteSerializer(result_page, many=True)      
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = CapacitacionDocenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({"mensaje": "Capacitación docente registrada correctamente.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de capacitacion."}, status=status.HTTP_400_BAD_REQUEST)
        
        capacitacion = get_object_or_404(CapacitacionDocente, pk=pk, usuario=request.user)
        serializer = CapacitacionDocenteSerializer(capacitacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Capacitación docente actualizada correctamente.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de capacitacion."}, status=status.HTTP_400_BAD_REQUEST)
        capacitacion = get_object_or_404(CapacitacionDocente, pk=pk, usuario=request.user)
        capacitacion.delete()
        return Response({"mensaje": "Capacitacion docente eliminada correctamente"}, status=status.HTTP_200_OK)

#Endpoint Actualizacion Diciplinaria
class ActualizacionDisciplinarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Devuelve las actualizaciones disciplinarias del usuario autenticado"""
        paginator = PageNumberPagination()
        paginator.page_size = 10
        if pk:
            actualizacion = get_object_or_404(ActualizacionDisciplinaria, pk=pk, usuario=request.user)
            serializer = ActualizacionDisciplinarSerializer(actualizacion)
            return Response(serializer.data)
        
        actualizaciones = ActualizacionDisciplinaria.objects.filter(usuario=request.user).order_by('anio_obtencion')
        result_page = paginator.paginate_queryset(actualizaciones, request)
        serializer = ActualizacionDisciplinarSerializer(result_page, many=True)        
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea una nueva actualización disciplinar para el usuario autenticado"""
        serializer = ActualizacionDisciplinarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({"mensaje": "Actualización disciplinar registrada correctamente.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza una actualización disciplinar existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de actualización disciplinar."}, status=status.HTTP_400_BAD_REQUEST)

        actualizacion = get_object_or_404(ActualizacionDisciplinaria, pk=pk, usuario=request.user)
        serializer = ActualizacionDisciplinarSerializer(actualizacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Actualización disciplinar actualizada correctamente.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina una actualización disciplinar existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de actualización disciplinar."}, status=status.HTTP_400_BAD_REQUEST)

        actualizacion = get_object_or_404(ActualizacionDisciplinaria, pk=pk, usuario=request.user)
        actualizacion.delete()
        return Response({"mensaje": "Actualización disciplinar eliminada correctamente."}, status=status.HTTP_200_OK)
    
#Endpoint para Gestion Academica
class GestionAcademicaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            gestion_academica = get_object_or_404(GestionAcademica, pk=pk, usuario=request.user)
            serializer = GestionAcademicaSerializer(gestion_academica)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        gestion_academica = GestionAcademica.objects.filter(usuario=request.user).order_by('d_mes_anio')
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Número de elementos por página
        resultado_paginado = paginator.paginate_queryset(gestion_academica, request)
        serializer = GestionAcademicaSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = GestionAcademicaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Gestión académica guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        gestion_academica = get_object_or_404(GestionAcademica, pk=pk, usuario=request.user)
        serializer = GestionAcademicaSerializer(gestion_academica, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Gestión académica actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        gestion_academica = get_object_or_404(GestionAcademica, pk=pk, usuario=request.user)
        gestion_academica.delete()
        return Response({'mensaje': 'Gestión académica eliminada correctamente.'}, status=status.HTTP_200_OK)
    
#Endpoint para Productos Academicos Relevantes
class ProductosAcademicosRelevantesView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: Listar todos los productos académicos del usuario autenticado
    def get(self, request):
        productos = ProductosAcademicosRelevantes.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Número de elementos por página
        resultado_paginado = paginator.paginate_queryset(productos, request)
        serializer = ProductosAcademicosRelevantesSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST: Crear un nuevo producto académico
    def post(self, request):
        serializer = ProductosAcademicosRelevantesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({'mensaje': 'Producto académico guardado correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Actualizar un producto académico existente
    def put(self, request, pk=None):
        producto = get_object_or_404(ProductosAcademicosRelevantes, pk=pk, usuario=request.user)
        serializer = ProductosAcademicosRelevantesSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Producto académico actualizado correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Eliminar un producto académico
    def delete(self, request, pk=None):
        producto = get_object_or_404(ProductosAcademicosRelevantes, pk=pk, usuario=request.user)
        producto.delete()
        return Response({"mensaje": "Producto académico eliminado correctamente."}, status=status.HTTP_200_OK)
    
#Endpoint para Experiencia Profesional no Academica
class ExperienciaProfesionalNoAcademicaView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: Listar todas las experiencias del usuario autenticado
    def get(self, request):
        experiencias = ExperienciaProfesionalNoAcademica.objects.filter(usuario=request.user).order_by('d_mes_anio')
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Número de elementos por página
        resultado_paginado = paginator.paginate_queryset(experiencias, request)
        serializer = ExperienciaProfesionalNoAcademicaSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST: Crear una nueva experiencia profesional
    def post(self, request):
        serializer = ExperienciaProfesionalNoAcademicaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({'mensaje': 'Experiencia profesional guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Actualizar una experiencia profesional existente
    def put(self, request, pk=None):
        experiencia = get_object_or_404(ExperienciaProfesionalNoAcademica, pk=pk, usuario=request.user)
        serializer = ExperienciaProfesionalNoAcademicaSerializer(experiencia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Experiencia profesional actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Eliminar una experiencia profesional
    def delete(self, request, pk=None):
        experiencia = get_object_or_404(ExperienciaProfesionalNoAcademica, pk=pk, usuario=request.user)
        experiencia.delete()
        return Response({"mensaje": "Experiencia profesional eliminada correctamente."}, status=status.HTTP_200_OK)
    
#Endpoint para Experiencia de Diseño Ingenieril
class ExperienciaDisenoIngenierilView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: Listar todas las experiencias en diseño ingenieril del usuario autenticado
    def get(self, request):
        experiencias = ExperienciaDisenoIngenieril.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Número de elementos por página
        resultado_paginado = paginator.paginate_queryset(experiencias, request)
        serializer = ExperienciaDisenoIngenierilSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST: Crear una nueva experiencia en diseño ingenieril
    def post(self, request):
        serializer = ExperienciaDisenoIngenierilSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({'mensaje': 'Experiencia en diseño ingenieril guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Actualizar una experiencia en diseño ingenieril existente
    def put(self, request, pk=None):
        experiencia = get_object_or_404(ExperienciaDisenoIngenieril, pk=pk, usuario=request.user)
        serializer = ExperienciaDisenoIngenierilSerializer(experiencia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Experiencia en diseño ingenieril actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Eliminar una experiencia en diseño ingenieril
    def delete(self, request, pk=None):
        experiencia = get_object_or_404(ExperienciaDisenoIngenieril, pk=pk, usuario=request.user)
        experiencia.delete()
        return Response({"mensaje": "Experiencia en diseño ingenieril eliminada correctamente."}, status=status.HTTP_200_OK)
    
#Endpoint para Logros Profesionales (No academicos)
class LogroProfesionalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todos los logros profesionales del usuario autenticado."""
        logros = LogrosProfesionales.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(logros, request)
        serializer = LogrosProfesionalesSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea un nuevo logro profesional para el usuario autenticado."""
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = LogrosProfesionalesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Logro profesional guardado correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza un logro profesional existente del usuario autenticado."""
        if not pk:
            return Response({"error": "Se requiere un ID de logro profesional."}, status=status.HTTP_400_BAD_REQUEST)

        logro = get_object_or_404(LogrosProfesionales, pk=pk, usuario=request.user)
        data = request.data.copy()
        data['usuario'] = request.user.id

        serializer = LogrosProfesionalesSerializer(logro, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Logro profesional actualizado correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina un logro profesional del usuario autenticado."""
        if not pk:
            return Response({"error": "Se requiere un ID de logro profesional."}, status=status.HTTP_400_BAD_REQUEST)

        logro = get_object_or_404(LogrosProfesionales, pk=pk, usuario=request.user)
        logro.delete()
        return Response({"mensaje": "Logro profesional eliminado correctamente."}, status=status.HTTP_200_OK)
    
#Endpoint para Participacion
class ParticipacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todas las participaciones del usuario autenticado"""
        participaciones = Participacion.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(participaciones, request)
        serializer = ParticipacionSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea una nueva participación para el usuario autenticado"""
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = ParticipacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Participación guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza una participación existente"""
        participacion = get_object_or_404(Participacion, pk=pk, usuario=request.user)
        serializer = ParticipacionSerializer(participacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Participación actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina una participación existente"""
        participacion = get_object_or_404(Participacion, pk=pk, usuario=request.user)
        participacion.delete()
        return Response({'mensaje': 'Participación eliminada correctamente.'}, status=status.HTTP_200_OK)

#Endpoint para Premio
class PremioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todos los premios del usuario autenticado"""
        premios = Premio.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(premios, request)
        serializer = PremioSerializer(premios, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea un nuevo premio para el usuario autenticado"""
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = PremioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Premio guardado correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza un premio existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de premio."}, status=status.HTTP_400_BAD_REQUEST)
        
        premio = Premio.objects.filter(pk=pk, usuario=request.user).first()
        if not premio:
            return Response({"error": "Premio no encontrado o no tienes permiso para editarlo."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PremioSerializer(premio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Premio actualizado correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina un premio existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de premio."}, status=status.HTTP_400_BAD_REQUEST)
        
        premio = Premio.objects.filter(pk=pk, usuario=request.user).first()
        if not premio:
            return Response({"error": "Premio no encontrado o no tienes permiso para eliminarlo."}, status=status.HTTP_404_NOT_FOUND)

        premio.delete()
        return Response({"mensaje": "Premio eliminado correctamente."}, status=status.HTTP_200_OK)

#Endpoint para Aportacion
class AportacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene todas las aportaciones del usuario autenticado"""
        aportaciones = Aportacion.objects.filter(usuario=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        resultado_paginado = paginator.paginate_queryset(aportaciones, request)
        serializer = AportacionSerializer(resultado_paginado, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Crea una nueva aportación para el usuario autenticado"""
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = AportacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Aportación guardada correctamente.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza una aportación existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de aportación."}, status=status.HTTP_400_BAD_REQUEST)
        
        aportacion = Aportacion.objects.filter(pk=pk, usuario=request.user).first()
        if not aportacion:
            return Response({"error": "Aportación no encontrada o no tienes permiso para editarla."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AportacionSerializer(aportacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Aportación actualizada correctamente.','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina una aportación existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de aportación."}, status=status.HTTP_400_BAD_REQUEST)
        
        aportacion = Aportacion.objects.filter(pk=pk, usuario=request.user).first()
        if not aportacion:
            return Response({"error": "Aportación no encontrada o no tienes permiso para eliminarla."}, status=status.HTTP_404_NOT_FOUND)

        aportacion.delete()
        return Response({"mensaje": "Aportación eliminada correctamente."}, status=status.HTTP_200_OK)
    
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
        
#Endpoint para Area de Adscripcion

    


    

