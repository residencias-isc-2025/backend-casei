from django.urls import path
from actualizacion_diciplinar.views import ActualizacionDisciplinarView

urlpatterns = [
    path('actualizacion-disciplinar/', ActualizacionDisciplinarView.as_view(), name='actualizacion_disciplinar'),
    path('actualizacion-disciplinar/<int:pk>/', ActualizacionDisciplinarView.as_view(), name='actualizacion_disciplinar_detail'),
]
