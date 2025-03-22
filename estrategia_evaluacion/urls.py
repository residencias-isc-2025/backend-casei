from django.urls import path
from estrategia_evaluacion.views import EstrategiaEvaluacionView

urlpatterns = [
    path('estrategia-evaluacion/', EstrategiaEvaluacionView.as_view(), name='estrategia-evaluacion'),
    path('estrategia-evaluacion/<int:pk>/', EstrategiaEvaluacionView.as_view(), name='estrategia-evaluacion-detail'),
]

