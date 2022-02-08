from django.db import models


class VideoUpload(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to="videos/")
