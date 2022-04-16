from questions import serializers as questions_serializers
from rest_framework import serializers as core_serializers

from . import models as video_models


class AttemptSerializer(core_serializers.ModelSerializer):
    class Meta:
        model = video_models.Attempt
        exclude = ["attempt_set", "video_file"]


class AttemptSetSerializer(core_serializers.ModelSerializer):
    user = questions_serializers.UserSerializer()
    attempt_set = AttemptSerializer(read_only=True, many=True)
    is_processed = core_serializers.SerializerMethodField()

    class Meta:
        model = video_models.AttemptSet
        fields = "__all__"

    def get_is_processed(self, obj):
        return obj.is_processed
