from rest_framework import viewsets

from . import models, serializers


class QuestionSetViewSet(viewsets.ModelViewSet):
    queryset = models.QuestionSet.objects.all()
    serializer_class = serializers.QuestionSetSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
