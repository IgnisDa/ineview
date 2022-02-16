from django.conf import settings
from django.db import models


class QuestionSet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="The user who created this set",
    )

    def __str__(self):
        return f"Question set by: {self.user}, ID: {self.id}"


class Question(models.Model):
    question_set = models.ForeignKey(
        QuestionSet,
        on_delete=models.CASCADE,
        help_text="The questions-set this question belongs to",
    )
    text = models.TextField(
        help_text="The actual question that will be displayed on screen"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="An optional description of the question",
    )

    def __str__(self):
        return f"Question set: {self.question_set}"
