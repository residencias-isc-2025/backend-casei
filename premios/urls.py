from django.urls import path
from premios.views import PremioView

urlpatterns = [
    path('premios/', PremioView.as_view(), name='premios'),
    path('premios/<int:pk>/', PremioView.as_view(), name='premio_detail'),
]
