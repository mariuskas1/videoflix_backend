from rest_framework import serializers
from django.conf import settings
from videoflix_app.models import Video
import os


class VideoSerializer(serializers.ModelSerializer):
    video_file_120p = serializers.SerializerMethodField()
    video_file_360p = serializers.SerializerMethodField()
    video_file_720p = serializers.SerializerMethodField()
    video_file_1080p = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_video_file_120p(self, obj):
        return self.get_video_url(obj.video_file, 120)

    def get_video_file_360p(self, obj):
        return self.get_video_url(obj.video_file, 360)

    def get_video_file_720p(self, obj):
        return self.get_video_url(obj.video_file, 720)

    def get_video_file_1080p(self, obj):
        return self.get_video_url(obj.video_file, 1080)

    def get_video_url(self, video_path, resolution):
        if not video_path:
            return None
        
        base_name = os.path.basename(video_path.name)  
        converted_path = f"media/videos/{base_name.replace('.mp4', f'_{resolution}p.mp4')}"
        
        
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, f"videos/{converted_path}")):
            return f"{settings.MEDIA_URL}{converted_path}"
        
        return None