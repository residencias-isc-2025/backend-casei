from django.urls import path

from registration.views import CustomAuthToken

urlpatterns = [
    # Usuarios
    
    # Institucion
    
    # Adscripcion
    
    # Formacion Academica

    # Capacitacion Docente
    
    
    # Actualizacion Disciplinar
    
    # Gestion Academica
    
    
    # Productos Academicos
    
    # Experiencia Profesional
    
    # Diseno Ingenieril
    
    # Logros Profesionales
    
    # Participacion
    
    # Premios
    
    # Aportaciones
    
    # Reportes
    
    path('api/token/', CustomAuthToken.as_view(), name='api_token_auth'),
]