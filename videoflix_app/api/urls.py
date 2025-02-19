from django.urls import path, include
from .views import VideoViewset
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'videos', VideoViewset)


urlpatterns = [
    path('', include(router.urls)),
]