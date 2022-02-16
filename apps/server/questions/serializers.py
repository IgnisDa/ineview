from rest_framework import serializers

from . import models


class QuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionSet
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = "__all__"
