from django.urls import path
from competencia.views import CompetenciaView

urlpatterns = [
    path('competencia/', CompetenciaView.as_view(), name='competencia'),
    path('competencia/<int:pk>/', CompetenciaView.as_view(), name='competencia-detail'),
]