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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from backendcasei.views import login_view

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('api/registration/', include('registration.urls')),

    # Paths de Auth
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('api/login/', login_view),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # URLS importantes 
    path('api/usuarios/', include('usuarios.urls')),
    path('api/institucion/', include('institucion.urls')),
    path('api/adscripcion/', include('adscripcion.urls')),
    path('api/formacion_academica/', include('formacion_academica.urls')),
    path('api/capacitacion_docente/', include('capacitacion_docente.urls')),
    path('api/actualizacion_diciplinar/', include('actualizacion_diciplinar.urls')),
    path('api/gestion_academica/', include('gestion_academica.urls')),
    path('api/productos_academicos/', include('productos_academicos.urls')),
    path('api/experiencia_profesional/', include('experiencia_profesional.urls')),
    path('api/experiencia_diseno/', include('experiencia_diseno.urls')),
    path('api/logros_profesionales/', include('logros_profesionales.urls')),
    path('api/participacion/', include('participacion.urls')),
    path('api/premios/', include('premios.urls')),
    path('api/aportaciones/', include('aportaciones.urls')),
    path('api/reportes/', include('reportes.urls')),
    path('api/periodos/', include('periodo.urls')),
    path('api/objetivos_especificos/', include('objetivos_especificos.urls')),
    path('api/atributo_egreso/', include('atributo_egreso.urls')),
    path('api/criterio_desempeno/', include('criterio_desempeno.urls')),
    path('api/estrategia_ensenanza/', include('estrategia_ensenanza.urls')),
    path('api/estrategia_evaluacion/', include('estrategia_evaluacion.urls')),
    path('api/practica/', include('practica.urls')),
    path('api/bibliografia/', include('bibliografia.urls')),
    path('api/temas/', include('temas.urls')),
    path('api/actividad_aprendizaje/', include('actividad_aprendizaje.urls')),
    path('api/competencias_genericas/', include('competencias_genericas.urls')),
    path('api/indicador_alcance/', include('indicador_alcance.urls')),
    path('api/nivel_desempenio/', include('nivel_desempenio.urls')),
    path('api/lista_cotejo/', include('lista_cotejo.urls')),
    path('api/sub_temas/', include('sub_temas.urls')),
    path('api/competencia/', include('competencia.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
