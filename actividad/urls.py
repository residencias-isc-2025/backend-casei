from django.urls import path
from actividad.views import ActividadView, ActividadesPorClaseView

urlpatterns = [
    path('actividad/', ActividadView.as_view(), name='actividades'),
    path('actividad/<int:pk>/', ActividadView.as_view(), name='actividad-detail'),
    path('clase/<int:clase_id>/actividades/', ActividadesPorClaseView.as_view(), name='actividades-por-clase'),
]