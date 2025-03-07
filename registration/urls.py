from django.urls import path
from .views import register, CurriculumVitaeView
from registration.views import RegisterUserView, CustomAuthToken, ResetPasswordView, ListUsersView, UserProfileView, UserFormacionAcademicaView, InstitucionPaisView, ChangePasswordView, CapacitacionDocenteView, ActualizacionDisciplinarView, GestionAcademicaView, ProductosAcademicosRelevantesView, ExperienciaProfesionalNoAcademicaView, ExperienciaDisenoIngenierilView, LogroProfesionalView, ParticipacionView, PremioView, AportacionView, CreateUsersByCsvView, HabilitarUsuarioView, HabilitarInstitucionView, AreaAdscripcionView, HabilitarAreaAdscripcionView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('api/token/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('users/', ListUsersView.as_view(), name='list_users'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('formacion-academica/', UserFormacionAcademicaView.as_view(), name='user_formacion_academica'),
    path('institucion-pais/', InstitucionPaisView.as_view(), name='institucion_pais'),
    path('institucion-pais/<int:pk>/', InstitucionPaisView.as_view(), name='institucion_pais_detail'),
    path('register/<int:pk>/', RegisterUserView.as_view(), name='register_user_detail'),  # Para PUT y DELETE
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('capacitacion-docente/', CapacitacionDocenteView.as_view(), name='capacitacion_docente'),
    path('capacitacion-docente/<int:pk>/', CapacitacionDocenteView.as_view(), name='capacitacion_docente_detail'),
    path('actualizacion-disciplinar/', ActualizacionDisciplinarView.as_view(), name='actualizacion_disciplinar'),
    path('actualizacion-disciplinar/<int:pk>/', ActualizacionDisciplinarView.as_view(), name='actualizacion_disciplinar_detail'),
    path('gestion-academica/', GestionAcademicaView.as_view(), name='gestion_academica'),
    path('gestion-academica/<int:pk>/', GestionAcademicaView.as_view(), name='gestion_academica_detail'),
    path('productos-academicos/', ProductosAcademicosRelevantesView.as_view(), name='productos_academicos'),
    path('productos-academicos/<int:pk>/', ProductosAcademicosRelevantesView.as_view(), name='productos_academicos_detail'),
    path('experiencia-profesional-no-academica/', ExperienciaProfesionalNoAcademicaView.as_view(), name='experiencia_profesional_no_academica'),
    path('experiencia-profesional-no-academica/<int:pk>/', ExperienciaProfesionalNoAcademicaView.as_view(), name='experiencia_profesional_no_academica_detail'),
    path('experiencia-diseno-ingenieril/', ExperienciaDisenoIngenierilView.as_view(), name='experiencia_diseno_ingenieril'),
    path('experiencia-diseno-ingenieril/<int:pk>/', ExperienciaDisenoIngenierilView.as_view(), name='experiencia_diseno_ingenieril_detail'),
    path('logros-profesionales/', LogroProfesionalView.as_view(), name='logros_profesionales'),
    path('logros-profesionales/<int:pk>/', LogroProfesionalView.as_view(), name='logros_profesionales_detail'),
    path('participacion/', ParticipacionView.as_view(), name='participacion'),
    path('participacion/<int:pk>/', ParticipacionView.as_view(), name='participacion_detail'),
    path('premios/', PremioView.as_view(), name='premios'),
    path('premios/<int:pk>/', PremioView.as_view(), name='premio_detail'),
    path('aportaciones/', AportacionView.as_view(), name='aportaciones'),
    path('aportaciones/<int:pk>/', AportacionView.as_view(), name='aportacion_detail'),

    path('curriculum-vitae/', CurriculumVitaeView.as_view(), name='all_tables'),

    path('create-users-by-csv/', CreateUsersByCsvView.as_view(), name='leer_csv'),
    path('habilitar-usuario/<int:pk>/', HabilitarUsuarioView.as_view(), name='habilitar_usuario'),
    path('habilitar-institucion/<int:pk>/', HabilitarInstitucionView.as_view(), name='habilitar_institucion'),
    path('reset-password/<int:pk>/', ResetPasswordView.as_view(), name='reset_password'),
    path('area-adscripcion/', AreaAdscripcionView.as_view(), name='area_adscripcion'),
    path('area-adscripcion/<int:pk>/', AreaAdscripcionView.as_view(), name='area_adscripcion_detail'),
    path('habilitar-area-adscripcion/<int:pk>/', HabilitarAreaAdscripcionView.as_view(), name='habilitar_area_adscripcion'),
    
]