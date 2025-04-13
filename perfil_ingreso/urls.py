from django.urls import path
from perfil_ingreso.views import PerfilIngresoView

urlpatterns = [
    path('perfil_ingreso/', PerfilIngresoView.as_view(), name='perfil-ingreso'),
    path('perfil_ingreso/<int:pk>/', PerfilIngresoView.as_view(), name='perfil-ingreso-detail'),
]