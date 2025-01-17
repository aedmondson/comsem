# Generated by Django 3.2 on 2023-02-14 00:13

import ComSemApp.models
from django.db import migrations, models
from ComSemApp.utils import transcribe_and_get_length_audio_file


def transcribe_audio_for_field(apps, schema_editor):
    speakingpracticeattempt = apps.get_model('ComSemApp','SpeakingPracticeAttempt')
    db_alias = schema_editor.connection.alias
    attempts : models.QuerySet[ComSemApp.models.SpeakingPracticeAttempt] = speakingpracticeattempt.objects.using(db_alias)
    for attempt in attempts:
        attempt.transcription, _ = transcribe_and_get_length_audio_file(attempt.audio)
        attempt.save()

class Migration(migrations.Migration):

    dependencies = [
        ('ComSemApp', '0025_auto_20230214_0013')
    ]

    operations = [
        migrations.RunPython(transcribe_audio_for_field)
    ]
