from django.urls import path
from formacion_academica.views import UserFormacionAcademicaView


urlpatterns = [
    path('formacion-academica/', UserFormacionAcademicaView.as_view(), name='user_formacion_academica'),
    path('formacion-academica/<int:pk>/', UserFormacionAcademicaView.as_view(), name='user_formacion_academica'),
]