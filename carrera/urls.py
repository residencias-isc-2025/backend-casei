from django.urls import path
from carrera.views import CarreraView, CarreraExportExcelView

urlpatterns = [
    path('carrera/', CarreraView.as_view(), name='carreras'),
    path('carrera/<int:pk>/', CarreraView.as_view(), name='carrera-detail'),
    path('carrera/exportar/', CarreraExportExcelView.as_view(), name='carrera-excel'),
]