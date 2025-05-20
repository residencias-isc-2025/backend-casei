from django.urls import path
from clase.views import ClaseView, MigrarClaseView, MisClasesView

urlpatterns = [
    path('clase/', ClaseView.as_view(), name='clases'),
    path('clase/<int:pk>/', ClaseView.as_view(), name='clase-detail'),
    path('clase/migrar/', MigrarClaseView.as_view()),
    path('clase/docente/', MisClasesView.as_view(), name='clase-docente'),

]