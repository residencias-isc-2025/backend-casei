from django.urls import path
from gestion_academica.views import GestionAcademicaView

urlpatterns = [
    path('gestion-academica/', GestionAcademicaView.as_view(), name='gestion_academica'),
    path('gestion-academica/<int:pk>/', GestionAcademicaView.as_view(), name='gestion_academica_detail'),
]
