from django.urls import path
from aportaciones.views import AportacionView

urlpatterns = [
    path('aportaciones/', AportacionView.as_view(), name='aportaciones'),
    path('aportaciones/<int:pk>/', AportacionView.as_view(), name='aportacion_detail'),
]
