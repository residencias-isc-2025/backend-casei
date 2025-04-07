from django.urls import path
from sub_temas.views import SubtemaView

urlpatterns = [
    path('sub-temas/', SubtemaView.as_view(), name='subtemas'),
    path('sub-temas/<int:pk>/', SubtemaView.as_view(), name='subtemas-detail'),
]