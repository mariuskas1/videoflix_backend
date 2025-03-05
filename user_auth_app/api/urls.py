from django.urls import path, include
from .views import RegistrationView, LoginView, UserView, TokenValidationView, ActivateAccountView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', UserView)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/validate/', TokenValidationView.as_view(), name='token_validate'),
    path('', include(router.urls)),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name="activate"),
]