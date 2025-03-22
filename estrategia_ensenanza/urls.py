from django.urls import path
from estrategia_ensenanza.views import EstrategiaEnsenanzaView

urlpatterns = [
    path('estrategias-ensenanza/', EstrategiaEnsenanzaView.as_view(), name='estrategias-ensenanza'),
    path('estrategias-ensenanza/<int:pk>/', EstrategiaEnsenanzaView.as_view(), name='estrategias-ensenanza-detail'),
]

