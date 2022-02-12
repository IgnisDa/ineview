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
        video = VideoUpload(video_file=file_obj)
        video.save()
        ffmpeg.input(video.video_file.path).output(f"{video.video_file.path}.mp4").run()
        video.video_file.name = (
            f"{video.video_file.name.replace(str(settings.MEDIA_ROOT), '')}.mp4"
        )
        video.save()
        return JsonResponse({"id": video.id})


class ProcessVideoView(APIView):
    def post(self, request, video_id):
        try:
            video = VideoUpload.objects.get(id=video_id)
        except VideoUpload.DoesNotExist:
            return JsonResponse({"status": False}, status=404)
        # TODO: Call code for processing the video
        video.is_processed = True
        video.save()
        return JsonResponse({"status": True})
