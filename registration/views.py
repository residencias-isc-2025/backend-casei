from registration.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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