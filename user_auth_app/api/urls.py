from django.urls import path, include
from .views import RegistrationView, LoginView, UserView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', UserView)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]