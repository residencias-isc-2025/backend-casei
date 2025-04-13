from django.urls import path
from actividad_aprendizaje.views import ActividadAprendizajeView

urlpatterns = [
    path('actividad-aprendizaje/', ActividadAprendizajeView.as_view(), name='actividad-aprendizaje'),
    path('actividad-aprendizaje/<int:pk>/', ActividadAprendizajeView.as_view(), name='actividad-aprendizaje-detail'),
]
