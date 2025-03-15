from django.urls import path
from .views import CurriculumVitaeView, CreateUsersByCsvView


urlpatterns = [
    path('curriculum-vitae/', CurriculumVitaeView.as_view(), name='all_tables'),
    path('cargar-usuarios-csv/', CreateUsersByCsvView.as_view(), name='cargar_usuarios_csv'),  # ✅ Agregamos esta línea

]
