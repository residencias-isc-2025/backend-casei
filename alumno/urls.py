from django.urls import path
from alumno.views import AlumnoView

urlpatterns = [
    path('alumno/', AlumnoView.as_view(), name='alumnos'),
    path('alumno/<int:pk>/', AlumnoView.as_view(), name='alumno-detail'),
]