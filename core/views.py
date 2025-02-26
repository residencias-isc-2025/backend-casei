from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render

def home(request):
    return render(request, "core/home.html")

def sample(request):
    return render(request, "core/sample.html")

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden hacer esto
def reset_password(request):
    """Permite a los superusuarios y administradores resetear la contraseña de un docente."""
    
    # Verifica que el usuario que solicita el cambio es admin o superusuario
    if not request.user.is_superuser and not request.user.is_staff:
        return Response({'error': 'No tienes permisos para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)

    # Recibe el nombre de usuario del docente desde el frontend
    username = request.data.get('username')

    try:
        # Busca al docente en la base de datos
        docente = User.objects.get(username=username)

        # Cambia la contraseña al nombre de usuario
        docente.set_password(username)
        docente.save()

        return Response({'message': f'La contraseña de {username} ha sido reseteada correctamente'}, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)