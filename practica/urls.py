from django.urls import path
from practica.views import PracticaView

urlpatterns = [
    path('practica/', PracticaView.as_view(), name='practica'),
    path('practica/<int:pk>/', PracticaView.as_view(), name='practica-detail')
]

