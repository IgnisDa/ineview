from django.contrib import admin

from .models import VideoUpload


@admin.register(VideoUpload)
class VideoAdmin(admin.ModelAdmin):
    pass
