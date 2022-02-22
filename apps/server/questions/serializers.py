from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "id", "email", "first_name", "last_name"]


class QuestionSerializer(serializers.ModelSerializer):
    answer_duration = serializers.SerializerMethodField()
    thinking_duration = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        exclude = ["question_set"]

    def get_answer_duration(self, obj):
        return obj.answer_duration.total_seconds()

    def get_thinking_duration(self, obj):
        return obj.thinking_duration.total_seconds()


class QuestionSetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    question_set = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = models.QuestionSet
        fields = "__all__"
