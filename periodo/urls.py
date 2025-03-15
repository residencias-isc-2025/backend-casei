from django.urls import path
from periodo.views import PeriodoView, ActivarPeriodoView

urlpatterns = [
    path('periodo/', PeriodoView.as_view(), name='periodo'),
    path('periodo/<int:pk>/', PeriodoView.as_view(), name='periodo_detail'),
    path('activar-periodo/<int:pk>/', ActivarPeriodoView.as_view(), name='activar_periodo'),
]