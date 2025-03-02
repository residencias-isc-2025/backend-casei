from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from registration.serializers import UserSerializer, FormacionAcademicaSerializer, InstitucionPaisSerializer, CapacitacionDocenteSerializer, ActualizacionDisciplinarSerializer
from registration.models import CustomUser, FormacionAcademica, InstitucionPais, CapacitacionDocente, ActualizacionDisciplinaria
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

# Enpoint De Registro
class RegisterUserView(APIView):
    permission_classes = [IsAuthenticated]  # 🔹 Solo usuarios autenticados pueden acceder

    def post(self, request):
        """Permite a Administradores y Super Usuarios crear cualquier tipo de usuario"""
        data = request.data

        # Verificar si el usuario que hace la solicitud es admin o superusuario
        if not request.user.is_staff:
            return Response({"mensaje": "No tienes permisos para crear usuarios."}, status=status.HTTP_403_FORBIDDEN)

        required_fields = ['username', 'password', 'role', 'apellido_materno', 'apellido_paterno', 'nombre', 'fecha_nacimiento']
        for field in required_fields:
            if field not in data:
                return Response({"mensaje": f"El campo '{field}' es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)

        username = data.get('username')
        password = make_password(data.get('password'))  # Hashear la contraseña
        role = data.get('role')
        apellido_materno = data.get('apellido_materno')
        apellido_paterno = data.get('apellido_paterno')
        nombre = data.get('nombre')
        fecha_nacimiento = data.get('fecha_nacimiento')
        tipo_docente = data.get('tipo_docente', None)

        #Validar si el Usuario ya existe
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "El nombre de usuario ya está registrado. Elige otro."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar que el rol sea válido
        if role not in ['superuser', 'admin', 'user']:
            return Response({"mensaje": "Rol inválido. Debe ser 'superuser', 'admin' o 'user'."},
                            status=status.HTTP_400_BAD_REQUEST)
        # Validar tipo_docente solo si el usuario es docente
        if role == 'user' and tipo_docente not in ['basificado', 'asignatura']:
            return Response({"error": "Si el usuario es 'user' (Docente), 'tipo_docente' debe ser 'basificado' o 'asignatura'."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.create(
                username=username, 
                password=password, 
                role=role,
                apellido_materno=apellido_materno,
                apellido_paterno=apellido_paterno,
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento
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
        """Permite actualizar la información de un usuario (solo admin/superuser)"""
        if not pk:
            return Response({"error": "Se requiere un ID de usuario."}, status=status.HTTP_400_BAD_REQUEST)

        usuario = get_object_or_404(CustomUser, pk=pk)

        if not request.user.is_staff:
            return Response({"error": "No tienes permisos para modificar usuarios."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        if "username" in data and data["username"] != usuario.username and CustomUser.objects.filter(username=data["username"]).exists():
            return Response({"error": "El nombre de usuario ya está registrado. Elige otro."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(usuario, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario actualizado correctamente", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Permite eliminar un usuario (solo admin/superuser)"""
        if not pk:
            return Response({"error": "Se requiere un ID de usuario."}, status=status.HTTP_400_BAD_REQUEST)

        usuario = get_object_or_404(CustomUser, pk=pk)

        if not request.user.is_staff:
            return Response({"error": "No tienes permisos para eliminar usuarios."}, status=status.HTTP_403_FORBIDDEN)

        usuario.delete()
        return Response({"mensaje": "Usuario eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)


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
        """Actualiza la contraseña del usuario autenticado"""
        usuario = request.user
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response({"error": "Ambos campos 'new_password' y 'confirm_password' son obligatorios."},
                            status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Las contraseñas no coinciden."}, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request):
        # Verificar si el usuario que hace la solicitud es admin o superusuario
        if not request.user.is_staff:
            return Response({"error": "No tienes permisos para resetear contraseñas."}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get("username")

        if not username:
            return Response({"error": "Se requiere el 'username' del docente."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)

            # Solo permitir resetear la contraseña de docentes
            if user.role != "user":
                return Response({"error": "Solo se puede resetear la contraseña de docentes."}, status=status.HTTP_403_FORBIDDEN)

            # Cambiar la contraseña al username del docente
            user.set_password(user.username)
            user.save()

            return Response({"message": f"La contraseña de {user.username} ha sido reseteada correctamente."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "No se encontró un usuario con ese username."}, status=status.HTTP_404_NOT_FOUND)
        
# Endpoint de listado
class ListUsersView(ListAPIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.exclude(id=self.request.user.id)
        return CustomUser.objects.none()
    
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
        
        formacion = FormacionAcademica.objects.filter(usuario=request.user)
        serializer = FormacionAcademicaSerializer(formacion, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        
        data = request.data.copy()  
        data["usuario"] = request.user.id

        serializer = FormacionAcademicaSerializer(data=data)
        if serializer.is_valid():
            serializer.save(usuario=request.user) 
            return Response(
                {"message": "Formación académica registrada correctamente.", "data": serializer.data},
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
            return Response({"message": "Información actualizada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# EndPoint para la Institucion y Pais
class InstitucionPaisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Devuelve la lista de todas las instituciones o una en específico si se pasa un ID."""
        if pk:
            institucion = get_object_or_404(InstitucionPais, pk=pk)
            serializer = InstitucionPaisSerializer(institucion)
            return Response(serializer.data)
        else:
            instituciones = InstitucionPais.objects.all()
            serializer = InstitucionPaisSerializer(instituciones, many=True)
            return Response(serializer.data)

    def post(self, request):
        """Permite registrar una nueva institución y país."""
        serializer = InstitucionPaisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Institución registrada correctamente.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Permite actualizar los datos de una institución."""
        if not pk:
            return Response({"error": "Se requiere un ID para actualizar una institución."}, status=status.HTTP_400_BAD_REQUEST)
        institucion = get_object_or_404(InstitucionPais, pk=pk)
        serializer = InstitucionPaisSerializer(institucion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Institución actualizada correctamente.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Permite eliminar una institución."""
        if not pk:
            return Response({"error": "Se requiere un ID para eliminar una institución."}, status=status.HTTP_400_BAD_REQUEST)

        institucion = get_object_or_404(InstitucionPais, pk=pk)
        institucion.delete()
        return Response({"message": "Institución eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)

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
        capacitaciones = CapacitacionDocente.objects.filter(usuario=request.user)
        serializer = CapacitacionDocenteSerializer(capacitaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CapacitacionDocenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de capacitacion."}, status=status.HTTP_400_BAD_REQUEST)
        
        capacitacion = get_object_or_404(CapacitacionDocente, pk=pk, usuario=request.user)
        serializer = CapacitacionDocenteSerializer(capacitacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Se requiere un ID de capacitacion."}, status=status.HTTP_400_BAD_REQUEST)
        capacitacion = get_object_or_404(CapacitacionDocente, pk=pk, usuario=request.user)
        capacitacion.delete()
        return Response({"mensaje": "Capacitacion eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)

#Endpoint Actualizacion Diciplinaria
class ActualizacionDisciplinarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Devuelve las actualizaciones disciplinarias del usuario autenticado"""
        if pk:
            actualizacion = get_object_or_404(ActualizacionDisciplinaria, pk=pk, usuario=request.user)
            serializer = ActualizacionDisciplinarSerializer(actualizacion)
            return Response(serializer.data)
        
        actualizaciones = ActualizacionDisciplinaria.objects.filter(usuario=request.user)
        serializer = ActualizacionDisciplinarSerializer(actualizaciones, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Crea una nueva actualización disciplinar para el usuario autenticado"""
        serializer = ActualizacionDisciplinarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Actualiza una actualización disciplinar existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de actualización disciplinar."}, status=status.HTTP_400_BAD_REQUEST)

        actualizacion = get_object_or_404(ActualizacionDisciplinaria, pk=pk, usuario=request.user)
        serializer = ActualizacionDisciplinarSerializer(actualizacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Elimina una actualización disciplinar existente del usuario autenticado"""
        if not pk:
            return Response({"error": "Se requiere un ID de actualización disciplinar."}, status=status.HTTP_400_BAD_REQUEST)

        actualizacion = get_object_or_404(ActualizacionDisciplinaria, pk=pk, usuario=request.user)
        actualizacion.delete()
        return Response({"mensaje": "Actualización disciplinar eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)
    
    