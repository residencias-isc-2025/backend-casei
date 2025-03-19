from django.urls import path
from carrera.views import CarreraView

urlpatterns = [
    path('carreras/', CarreraView.as_view(), name='carreras'),
    path('carreras/<int:pk>/', CarreraView.as_view(), name='carrera-detail'),
]