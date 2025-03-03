from django.urls import path
from .views import register
from registration.views import RegisterUserView, CustomAuthToken, ResetPasswordView, ListUsersView, UserProfileView, UserFormacionAcademicaView, InstitucionPaisView, ChangePasswordView, CapacitacionDocenteView, ActualizacionDisciplinarView, GestionAcademicaView, ProductosAcademicosRelevantesView, ExperienciaProfesionalNoAcademicaView, ExperienciaDiseñoIngenierilView, LogroProfesionalView

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
    path('experiencia-diseno-ingenieril/', ExperienciaDiseñoIngenierilView.as_view(), name='experiencia_diseño_ingenieril'),
    path('experiencia-diseno-ingenieril/<int:pk>/', ExperienciaDiseñoIngenierilView.as_view(), name='experiencia_diseño_ingenieril_detail'),
    path('logros-profesionales/', LogroProfesionalView.as_view(), name='logros_profesionales'),
    path('logros-profesionales/<int:pk>/', LogroProfesionalView.as_view(), name='logros_profesionales_detail'),
]