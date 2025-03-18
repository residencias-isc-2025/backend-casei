from django.urls import path
from objetivos_especificos.views import ObjetivoEspecificoView

urlpatterns = [
    path('objetivos-especificos/', ObjetivoEspecificoView.as_view(), name='objetivos-especificos'),
    path('objetivos-especificos/<int:pk>/', ObjetivoEspecificoView.as_view(), name='objetivos-especificos-detail'),
]
