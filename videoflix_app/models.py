from django.db import models
from datetime import date


GENRES = [
    ('documentary', 'Documentary'),
    ('drama', 'Drama'),
    ('romance', 'Romance'),
]

class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    genre = models.CharField(max_length=80, choices=GENRES, default='documentary')
    description = models.CharField(max_length=500, blank=True, null=True)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.FileField(upload_to='thumbnails', null=True, blank=True)
    new = models.BooleanField(default=False)

    def __str__(self):
        return self.title