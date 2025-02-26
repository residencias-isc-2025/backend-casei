from django.urls import path, include
from . import views
from core.views import reset_password

urlpatterns = [
    path('', views.home, name="home"),
    path('sample/', views.sample, name="sample"),
    path('reset-password/', reset_password, name='reset_password'),

    path('registration/', include('registration.urls')),
]