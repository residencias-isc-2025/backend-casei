from django.urls import path
from .views import register
from registration.views import RegisterUserView, CustomAuthToken, ResetPasswordView, ListUsersView, UserProfileView, UserFormacionAcademicaView, NombreProfesorView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('api/token/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('users/', ListUsersView.as_view(), name='list_users'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('formacion-academica/', UserFormacionAcademicaView.as_view(), name='user_formacion_academica'),
    path('nombre-profesor/', NombreProfesorView.as_view(), name='nombre_profesor'),
]