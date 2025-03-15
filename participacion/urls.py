from django.urls import path
from participacion.views import ParticipacionView

urlpatterns = [
    path('participacion/', ParticipacionView.as_view(), name='participacion'),
    path('participacion/<int:pk>/', ParticipacionView.as_view(), name='participacion_detail'),
]
