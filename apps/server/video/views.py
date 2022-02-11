from datetime import datetime

import ffmpeg
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import VideoUpload


class VideoUploadView(APIView):
    def post(self, request):
        file_obj = request.data["file"]
        file_obj.name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.webm"
        vu = VideoUpload(video_file=file_obj)
        vu.save()
        ffmpeg.input(vu.video_file.path).output(f"{vu.video_file.path}.mp4").run()
        vu.video_file.name = (
            f"{vu.video_file.name.replace(str(settings.MEDIA_ROOT), '')}.mp4"
        )
        vu.save()
        return JsonResponse({"id": vu.id})
