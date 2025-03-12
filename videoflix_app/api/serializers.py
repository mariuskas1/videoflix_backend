from rest_framework import serializers
from django.conf import settings
from videoflix_app.models import Video
import os


class VideoSerializer(serializers.ModelSerializer):
    """ This serializer automatically creates the urls for the other video-resolutions according to the uploaded file field."""
    
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

    def get_video_url(self, video_file, resolution):
        if not video_file:
            return None
        
        # Extract filename from FileField
        base_name = os.path.basename(video_file.name)  
        converted_filename = base_name.replace('.mp4', f'_{resolution}p.mp4')

        # Construct the relative path under media
        converted_path = f"videos/{converted_filename}"  

        # Construct the absolute file path to check existence
        full_path = os.path.join(settings.MEDIA_ROOT, converted_path)

        # Only return the URL if the file actually exists
        if os.path.exists(full_path):
            return f"{settings.MEDIA_URL}{converted_path}"
        
        return None