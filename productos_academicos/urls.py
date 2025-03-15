from django.urls import path
from productos_academicos.views import ProductosAcademicosRelevantesView

urlpatterns = [
    path('productos-academicos/', ProductosAcademicosRelevantesView.as_view(), name='productos_academicos'),
    path('productos-academicos/<int:pk>/', ProductosAcademicosRelevantesView.as_view(), name='productos_academicos_detail'),
    
]
