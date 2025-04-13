from django.urls import path
from atributo_egreso.views import AtributoEgresoView

urlpatterns = [
    path('atributos-egreso/', AtributoEgresoView.as_view(), name='atributos-egreso'),
    path('atributos-egreso/<int:pk>/', AtributoEgresoView.as_view(), name='atributos-egreso-detail')
]
