from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken  # 🔹 Importación para autenticación por tokens
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from registration.serializers import UserSerializer
from registration.models import CustomUser
from django.shortcuts import render, redirect
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

        required_fields = ['username', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return Response({"mensaje": f"El campo '{field}' es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)

        username = data.get('username')
        password = make_password(data.get('password'))  # Hashear la contraseña
        role = data.get('role')
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
            user = CustomUser.objects.create(username=username, password=password, role=role)

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
            return CustomUser.objects.all()
        return CustomUser.objects.none()
    
# Endpoint de jalar la informacion del usuario autenticado
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


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
