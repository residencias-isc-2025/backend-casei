from django.urls import path
from perfil_egreso.views import PerfilEgresoView

urlpatterns = [
    path('perfil_egreso/', PerfilEgresoView.as_view(), name='perfil-egreso'),
    path('perfil_egreso/<int:pk>/', PerfilEgresoView.as_view(), name='perfil-egreso-detail'),
]