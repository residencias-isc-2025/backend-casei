from django.urls import path
from institucion.views import (
    InstitucionPaisView, HabilitarInstitucionView
)

urlpatterns = [
    path('institucion-pais/', InstitucionPaisView.as_view(), name='institucion_pais'),
    path('institucion-pais/<int:pk>/', InstitucionPaisView.as_view(), name='institucion_pais_detail'),
    path('habilitar-institucion/<int:pk>/', HabilitarInstitucionView.as_view(), name='habilitar_institucion'),
]