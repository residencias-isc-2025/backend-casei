from django.urls import path
from criterio_desempeno.views import CriterioDesempenoView

urlpatterns = [
    path('criterio-desempeno/', CriterioDesempenoView.as_view(), name='criterio-desempeno'),
    path('criterio-desempeno/<int:pk>/', CriterioDesempenoView.as_view(), name='criterio-desempeno-detail')
]
