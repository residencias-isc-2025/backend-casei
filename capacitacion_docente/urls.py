from django.urls import path
from capacitacion_docente.views import CapacitacionDocenteView

urlpatterns = [
    path('capacitacion-docente/', CapacitacionDocenteView.as_view(), name='capacitacion_docente'),
    path('capacitacion-docente/<int:pk>/', CapacitacionDocenteView.as_view(), name='capacitacion_docente_detail'),
]
