from django.urls import path
from alumno.views import AlumnoView, AlumnoCountView, HablitarAlumnoView, AlumnosByCsv

urlpatterns = [
    path('alumno/', AlumnoView.as_view(), name='alumnos'),
    path('alumno/<int:pk>/', AlumnoView.as_view(), name='alumno-detail'),
    path('alumno/habilitar/<int:pk>/', HablitarAlumnoView.as_view(), name='alumno-detail'),
    path('alumno/count/', AlumnoCountView.as_view(), name='alumno-count'),
    path('alumno/carga-csv/', AlumnosByCsv.as_view(), name='alumno-csv')
    
]