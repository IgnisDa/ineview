from datetime import datetime

import ffmpeg
from django.conf import settings
from django.http import JsonResponse
from questions import models as questions_models
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from . import emotion_recognition, models, serializers


class AttemptSetViewSet(viewsets.ModelViewSet):
    queryset = models.AttemptSet.objects.all()
    serializer_class = serializers.AttemptSetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        instance = models.AttemptSet.objects.create(user=request.user)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateAttemptView(APIView):
    def post(self, request, *args, **kwargs):
        question_set_id = kwargs["question_set_id"]
        attempt_set_id = kwargs["attempt_set_id"]
        attempt_set = models.AttemptSet.objects.get(id=attempt_set_id)
        question = questions_models.Question.objects.get(id=question_set_id)
        file_obj = request.data["file"]
        file_obj.name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.webm"
        instance = models.Attempt.objects.create(
            video_file=file_obj, attempt_set=attempt_set, question=question
        )
        (
            ffmpeg.input(instance.video_file.path)
            .filter("fps", fps=1, round="up")
            .output(f"{instance.video_file.path}.mp4")
            .run()
        )
        instance.video_file.name = (
            f"{instance.video_file.name.replace(str(settings.MEDIA_ROOT), '')}.mp4"
        )
        instance.save()
        return JsonResponse({"id": instance.id})


class ProcessAttemptSetView(APIView):
    def post(self, request, attempt_set_id):
        try:
            attempt_set = models.AttemptSet.objects.get(id=attempt_set_id)
        except models.AttemptSet.DoesNotExist:
            return JsonResponse({"status": False}, status=404)
        final_data = []
        for attempt in attempt_set.attempt_set.all():
            if attempt.is_processed:
                data = attempt.data
            else:
                data = emotion_recognition.process_video(
                    attempt.video_file.path, attempt.id
                )
                attempt.is_processed = True
                attempt.data = data
                attempt.save()
            final_data.append(data)
        return JsonResponse({"status": True, "data": final_data})
