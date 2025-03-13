from django.urls import path, include
from usuarios.views import (
    RegisterUserView, ChangePasswordView, ResetPasswordView, ListUsersView, UserProfileView,
    CreateUsersByCsvView, HabilitarUsuarioView
)
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('register/<int:pk>/', RegisterUserView.as_view(), name='register_user_detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password/<int:pk>/', ResetPasswordView.as_view(), name='reset_password'),
    path('users/', ListUsersView.as_view(), name='list_users'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('create-users-by-csv/', CreateUsersByCsvView.as_view(), name='leer_csv'),
    path('habilitar-usuario/<int:pk>/', HabilitarUsuarioView.as_view(), name='habilitar_usuario'),
]