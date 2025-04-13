from django.urls import path
from competencias_genericas.views import CompetenciaGenericaView

urlpatterns = [
    path('competencias-genericas/', CompetenciaGenericaView.as_view(), name='competencias-genericas'),
    path('competencias-genericas/<int:pk>/', CompetenciaGenericaView.as_view(), name='competencias-genericas-detail'),
]