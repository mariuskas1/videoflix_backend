from rest_framework import serializers
from django.conf import settings
from videoflix_app.models import Video
import os


class VideoSerializer(serializers.ModelSerializer):
    """ This serializer automatically creates the urls for every video-resolution
      according to the file name in the file_field."""

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

        # Construct the full absolute URL
        full_url = f"{settings.MEDIA_URL}videos/{converted_filename}"

        # Ensure the URL is properly formatted with the full domain
        request = self.context.get('request', None)
        if request:
            return request.build_absolute_uri(full_url)
        
        # Fallback if request context is not available
        return full_url