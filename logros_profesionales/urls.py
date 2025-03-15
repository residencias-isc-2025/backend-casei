from django.urls import path
from logros_profesionales.views import LogroProfesionalView

urlpatterns = [
    path('logros-profesionales/', LogroProfesionalView.as_view(), name='logros_profesionales'),
    path('logros-profesionales/<int:pk>/', LogroProfesionalView.as_view(), name='logros_profesionales_detail'),
]
