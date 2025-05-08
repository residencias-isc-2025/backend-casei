from django.urls import path
from estrategia_ensenanza.views import EstrategiaEnsenanzaView

urlpatterns = [
    path('estrategia-ensenanza/', EstrategiaEnsenanzaView.as_view(), name='estrategias-ensenanza'),
    path('estrategia-ensenanza/<int:pk>/', EstrategiaEnsenanzaView.as_view(), name='estrategias-ensenanza-detail'),
]

