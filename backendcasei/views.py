from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json

def hello_world(request, param1, param2):
    return JsonResponse({
        "param1": param1,
        "param2": param2,
        "mensaje": "Datos recibidos correctamente"
        })
    
    
    
@csrf_exempt 
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                return JsonResponse({"mensaje": "Inicio de sesión exitoso"}, status=200)
            else:
                return JsonResponse({"mensaje": "Credenciales incorrectas"}, status=401)
            
        except json.JSONDecodeError:
            return JsonResponse({"mensaje": "Datos inválidos"}, status=400)
        