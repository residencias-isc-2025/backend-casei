from django.urls import path
from indicador_alcance.views import IndicadorAlcanceView

urlpatterns = [
    path('indicador-alcance/', IndicadorAlcanceView.as_view(), name='indicador-alcance'),
    path('indicador-alcance/<int:pk>/', IndicadorAlcanceView.as_view(), name='indicador-alcance-detail'),
]