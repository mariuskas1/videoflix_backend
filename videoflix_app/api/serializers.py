from rest_framework import serializers
from videoflix_app.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

    def to_representation(self, instance):
        """Customize serialized output to conditionally include 'video_file'."""
        representation = super().to_representation(instance)

        request = self.context.get('request')
        if request and request.parser_context:
            if request.parser_context['view'].action == 'list':
                representation.pop('video_file', None)

        return representation