from rest_framework import viewsets
from videoflix_app.models import Video
from .serializers import VideoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny



class VideoViewset(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}