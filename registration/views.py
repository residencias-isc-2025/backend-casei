import csv
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from registration.models import CustomUser
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

#Endpoint Actualizacion Diciplinaria

#Endpoint para Gestion Academica

#Endpoint para Productos Academicos Relevantes
    
#Endpoint para Experiencia Profesional no Academica

#Endpoint para Experiencia de Diseño Ingenieril
    
#Endpoint para Logros Profesionales (No academicos)

#Endpoint para Participacion

#Endpoint para Premio


#Endpoint para Aportacion

    
        
#Endpoint para Area de Adscripcion

    


    

