from django.urls import path
from experiencia_diseno.views import ExperienciaDisenoIngenierilView

urlpatterns = [
    path('experiencia-diseno-ingenieril/', ExperienciaDisenoIngenierilView.as_view(), name='experiencia_diseno_ingenieril'),
    path('experiencia-diseno-ingenieril/<int:pk>/', ExperienciaDisenoIngenierilView.as_view(), name='experiencia_diseno_ingenieril_detail'),
]
