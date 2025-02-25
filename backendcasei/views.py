from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                tokens = get_tokens_for_user(user)
                return JsonResponse({"mensaje": "Inicio de sesión exitoso", "tokens": tokens}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"mensaje": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)
            
        except json.JSONDecodeError:
            return JsonResponse({"mensaje": "Datos inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        