from django.urls import path
from donde_trabaja.views import DondeTrabajaView

urlpatterns = [
    path('donde_trabaja/', DondeTrabajaView.as_view(), name='donde-trabaja'),
    path('donde_trabaja/<int:pk>/', DondeTrabajaView.as_view(), name='donde-trabaja-detail'),
]