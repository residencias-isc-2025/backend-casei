from django.urls import path
from objetivos_educacionales.views import ObjetivoEducacionalView

urlpatterns = [
    path('objetivos_educacionales/', ObjetivoEducacionalView.as_view(), name='objetivos-educacionales'),
    path('objetivos_educacionales/<int:pk>/', ObjetivoEducacionalView.as_view(), name='objetivo-educacional-detail'),
]