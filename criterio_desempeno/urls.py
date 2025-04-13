from django.urls import path
from criterio_desempeno.views import CriterioDesempenoView

urlpatterns = [
    path('criterios-desempeno/', CriterioDesempenoView.as_view(), name='criterios-desempeno'),
    path('criterios-desempeno/<int:pk>/', CriterioDesempenoView.as_view(), name='criterios-desempeno-detail'),
]
