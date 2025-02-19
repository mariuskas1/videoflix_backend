from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Video



class VideoResource(resources.ModelResource):
    class Meta:
        model = Video


class VideoAdmin(ImportExportModelAdmin):
    resource_class = VideoResource

admin.site.register(Video, VideoAdmin)