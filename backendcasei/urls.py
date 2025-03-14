"""
URL configuration for backendcasei project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from backendcasei.views import login_view

urlpatterns = [
    path('', include('core.urls')),

    # URLS importantes 
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('institucion/', include('institucion.urls')),
    path('adscripcion/', include('adscripcion.urls')),

    # Paths de Auth
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('api/login/', login_view),
    path('api/registration/', include('registration.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
