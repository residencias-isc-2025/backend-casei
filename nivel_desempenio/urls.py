from django.urls import path
from nivel_desempenio.views import NivelDesempenioView

urlpatterns = [
    path('nivel-desempenio/', NivelDesempenioView.as_view(), name='nivel-desempenio'),
    path('nivel-desempenio/<int:pk>/', NivelDesempenioView.as_view(), name='nivel-desempenio-detail'),
]