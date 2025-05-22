from django.urls import path
from calificaciones.views import CalificacionView, CalificacionesPorClaseView

urlpatterns = [
    path('calificaciones/', CalificacionView.as_view(), name='calificaciones'),
    path('calificaciones/<int:pk>/', CalificacionView.as_view(), name='calificacion-detail'),
    path('clase/<int:clase_id>/calificaciones/', CalificacionesPorClaseView.as_view(), name='calificaciones-clase'),
]