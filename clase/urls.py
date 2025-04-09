from django.urls import path
from clase.views import ClaseView

urlpatterns = [
    path('clase/', ClaseView.as_view(), name='clases'),
    path('clase/<int:pk>/', ClaseView.as_view(), name='clase-detail'),
]