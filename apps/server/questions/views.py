from django.forms.models import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response

from . import models, serializers


class QuestionSetViewSet(viewsets.ModelViewSet):
    queryset = models.QuestionSet.objects.all()
    serializer_class = serializers.QuestionSetSerializer

    def retrieve(self, request, pk=None):
        question_set = models.QuestionSet.objects.get(id=pk)
        questions = models.Question.objects.filter(question_set_id=pk)
        response = model_to_dict(question_set)
        response["questions"] = serializers.QuestionSerializer(
            questions, many=True
        ).data
        return Response(response)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
