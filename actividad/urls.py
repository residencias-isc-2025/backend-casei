from django.urls import path
from actividad.views import ActividadView

urlpatterns = [
    path('actividad/', ActividadView.as_view(), name='actividades'),
    path('actividad/<int:pk>/', ActividadView.as_view(), name='actividad-detail'),
]