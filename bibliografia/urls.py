from django.urls import path
from bibliografia.views import BibliografiaView

urlpatterns = [
    path('bibliografia/', BibliografiaView.as_view(), name='bibliografia'),
    path('bibliografia/<int:pk>/', BibliografiaView.as_view(), name='bibliografia-detail'),
]