from django.urls import path
from calificaciones.views import CalificacionView

urlpatterns = [
    path('calificaciones/', CalificacionView.as_view(), name='calificaciones'),
    path('calificaciones/<int:pk>/', CalificacionView.as_view(), name='calificacion-detail'),
]