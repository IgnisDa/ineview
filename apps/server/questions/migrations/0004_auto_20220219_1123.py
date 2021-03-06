# Generated by Django 3.2 on 2022-02-19 11:23

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0003_rename_descriptions_question_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="answer_duration",
            field=models.DurationField(
                default=datetime.timedelta(seconds=60),
                help_text="The amount of time that would be given to answer this question",
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="thinking_duration",
            field=models.DurationField(
                default=datetime.timedelta(seconds=30),
                help_text="The amount of time that would be given to think about this question",
            ),
        ),
    ]
