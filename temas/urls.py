from django.urls import path
from temas.views import TemasView

urlpatterns = [
    path('temas/', TemasView.as_view(), name='temas'),
    path('temas/<int:pk>/', TemasView.as_view(), name='temas-detail'),
]

