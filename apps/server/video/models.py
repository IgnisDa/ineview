from django.db import models


class VideoUpload(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to="videos/")
    is_processed = models.BooleanField(
        default=False, help_text="Whether this video file has been processed yet"
    )

    def __str__(self):
        return f"{self.video_file.name}"
