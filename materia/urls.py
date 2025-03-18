from django.urls import path
from materia.views import MateriaView

urlpatterns = [
    path('materia/', MateriaView.as_view(), name='materias'),
    path('materia/<int:pk>/', MateriaView.as_view(), name='materias-detail'),
]