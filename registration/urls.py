from django.urls import path
from .views import CurriculumVitaeView
from registration.views import CustomAuthToken, ExperienciaProfesionalNoAcademicaView, ExperienciaDisenoIngenierilView, LogroProfesionalView, ParticipacionView, PremioView, AportacionView

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
    path('experiencia-profesional-no-academica/', ExperienciaProfesionalNoAcademicaView.as_view(), name='experiencia_profesional_no_academica'),
    path('experiencia-profesional-no-academica/<int:pk>/', ExperienciaProfesionalNoAcademicaView.as_view(), name='experiencia_profesional_no_academica_detail'),
    
    # Diseno Ingenieril
    path('experiencia-diseno-ingenieril/', ExperienciaDisenoIngenierilView.as_view(), name='experiencia_diseno_ingenieril'),
    path('experiencia-diseno-ingenieril/<int:pk>/', ExperienciaDisenoIngenierilView.as_view(), name='experiencia_diseno_ingenieril_detail'),
    
    # Logros Profesionales
    path('logros-profesionales/', LogroProfesionalView.as_view(), name='logros_profesionales'),
    path('logros-profesionales/<int:pk>/', LogroProfesionalView.as_view(), name='logros_profesionales_detail'),
    
    # Participacion
    path('participacion/', ParticipacionView.as_view(), name='participacion'),
    path('participacion/<int:pk>/', ParticipacionView.as_view(), name='participacion_detail'),
    
    # Premios
    path('premios/', PremioView.as_view(), name='premios'),
    path('premios/<int:pk>/', PremioView.as_view(), name='premio_detail'),
    
    # Aportaciones
    path('aportaciones/', AportacionView.as_view(), name='aportaciones'),
    path('aportaciones/<int:pk>/', AportacionView.as_view(), name='aportacion_detail'),
    
    # Reportes
    path('curriculum-vitae/', CurriculumVitaeView.as_view(), name='all_tables'),
    
    path('api/token/', CustomAuthToken.as_view(), name='api_token_auth'),
]