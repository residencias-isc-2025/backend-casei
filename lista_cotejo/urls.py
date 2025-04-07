from django.urls import path
from lista_cotejo.views import ListaCotejoView

urlpatterns = [
    path('lista-cotejo/', ListaCotejoView.as_view(), name='lista-cotejo'),
    path('lista-cotejo/<int:pk>/', ListaCotejoView.as_view(), name='lista-cotejo-detail'),
]