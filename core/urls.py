from django.urls import path, include
from . import views
from core.views import reset_password

urlpatterns = [
    path('', views.home, name="home"),
    path('sample/', views.sample, name="sample"),
    path('reset-password/', reset_password, name='reset_password'),

    path('usuarios/', include('usuarios.urls')),
    path('institucion/', include('institucion.urls')),
    path('adscripcion/', include('adscripcion.urls')),
]