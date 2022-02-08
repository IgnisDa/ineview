from django.http import JsonResponse
from rest_framework.views import APIView

from .models import VideoUpload


class VideoUploadView(APIView):
    def post(self, request):
        video = request.FILES["file"]
        video.name = "file.webm"
        vu = VideoUpload(video_file=video)
        vu.save()
        return JsonResponse({"id": vu.id})
