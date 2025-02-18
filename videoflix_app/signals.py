from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
from videoflix_app.tasks import convert_720p


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Ok Video')

    if created:
        print('Video created')
        convert_720p(instance.video_file.path)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, created, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)