import subprocess
import os
from videoflix_app.models import Video 
from django.core.files import File
from django.conf import settings


def convert_video(input_path, output_path, resolution):
    command = [
        'ffmpeg', '-i', input_path, '-vf', f"scale=-2:{resolution}",
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-c:a', 'aac', '-b:a', '128k', output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def update_video_field(video, resolution, output_path):
    """ Update the database with the new video file. """
    field_map = {
        120: 'video_file_120p',
        360: 'video_file_360p',
        720: 'video_file_720p',
        1080: 'video_file_1080p'
    }

    field_name = field_map.get(resolution)
    if field_name:
        setattr(video, field_name, output_path.replace(settings.MEDIA_ROOT, ''))
        video.save()


def convert_120p(input_path):
    output_path = input_path.replace('.mp4', '_120p.mp4')
    convert_video(input_path, output_path, 120)

    video = Video.objects.filter(video_file=input_path.replace(settings.MEDIA_ROOT, '')).first()
    if video:
        update_video_field(video, 120, output_path)


def convert_360p(input_path):
    output_path = input_path.replace('.mp4', '_360p.mp4')
    convert_video(input_path, output_path, 360)

    video = Video.objects.filter(video_file=input_path.replace(settings.MEDIA_ROOT, '')).first()
    if video:
        update_video_field(video, 360, output_path)


def convert_720p(input_path):
    output_path = input_path.replace('.mp4', '_720p.mp4')
    convert_video(input_path, output_path, 720)

    video = Video.objects.filter(video_file=input_path.replace(settings.MEDIA_ROOT, '')).first()
    if video:
        update_video_field(video, 720, output_path)


def convert_1080p(input_path):
    output_path = input_path.replace('.mp4', '_1080p.mp4')
    convert_video(input_path, output_path, 1080)

    video = Video.objects.filter(video_file=input_path.replace(settings.MEDIA_ROOT, '')).first()
    if video:
        update_video_field(video, 1080, output_path)
