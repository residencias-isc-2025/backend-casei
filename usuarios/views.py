import csv
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from usuarios.models import CustomUser
from usuarios.serializers import UserSerializer
from django.contrib.auth.hashers import make_password

from registration.models import AreaAdscripcion
# Create your views here.

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
        
# Endpoint de jalar la informacion del usuario autenticado
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Endpoint de listado
class ListUsersView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        # Excluir al usuario actual siempre
        queryset = CustomUser.objects.exclude(id=self.request.user.id).order_by('username')

        # Si el usuario es admin, excluir superusers
        if self.request.user.role == 'admin':
            queryset = queryset.exclude(role='superuser')

        # Filtros de búsqueda
        search_username = self.request.query_params.get('username', None)
        search_name = self.request.query_params.get('nombre', None)
        search_area_adscripcion = self.request.query_params.get('area_adscripcion', None)
        search_estado = self.request.query_params.get('estado', None)

        if search_username:
            queryset = queryset.filter(username__startswith=search_username)
        if search_name:
            queryset = queryset.filter(nombre__startswith=search_name)
        if search_area_adscripcion:
            try:
                area_adscripcion_id = int(search_area_adscripcion)
                queryset = queryset.filter(area_adscripcion__id=area_adscripcion_id)
            except ValueError:
                pass
        if search_estado:
            queryset = queryset.filter(estado__exact=search_estado)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
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

                    # Validar área de adscripción
                    area_adscripcion_id = fila.get('area_adscripcion', None)
                    area_adscripcion = None
                    if area_adscripcion_id:
                        if not area_adscripcion_id.isdigit():  # Verifica si es un número
                            errores.append(f"El área de adscripción '{area_adscripcion_id}' no es un ID válido.")
                            continue
                        try:
                            area_adscripcion = AreaAdscripcion.objects.get(id=int(area_adscripcion_id))
                        except AreaAdscripcion.DoesNotExist:
                            errores.append(f"El área de adscripción con ID {area_adscripcion_id} no existe.")
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
                        area_adscripcion=area_adscripcion,
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
        


        