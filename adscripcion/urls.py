from django.urls import path, include
from adscripcion.views import AreaAdscripcionView, HabilitarAreaAdscripcionView, AdscripcionByCsvView

urlpatterns = [
    path('area-adscripcion/', AreaAdscripcionView.as_view(), name='area_adscripcion'),
    path('area-adscripcion/<int:pk>/', AreaAdscripcionView.as_view(), name='area_adscripcion_detail'),
    path('area-adscripcion/carga-csv/', AdscripcionByCsvView.as_view(), name='area_adscripcion_csv'),
    path('habilitar-area-adscripcion/<int:pk>/', HabilitarAreaAdscripcionView.as_view(), name='habilitar_area_adscripcion'),
]
