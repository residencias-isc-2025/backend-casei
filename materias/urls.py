from django.urls import path
from materias.views import MateriaView

urlpatterns = [
    path('materias/', MateriaView.as_view(), name='materias'),
    path('materias/<int:pk>/', MateriaView.as_view(), name='materia-detail'),
]