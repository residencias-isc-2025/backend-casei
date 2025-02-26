from django.urls import path
from .views import register
from registration.views import RegisterUserView, CustomAuthToken

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('api/token/', CustomAuthToken.as_view(), name='api_token_auth'),
]