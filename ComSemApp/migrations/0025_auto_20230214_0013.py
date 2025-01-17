# Generated by Django 3.2 on 2023-02-14 00:13

import django.core.validators
import ComSemApp.models
from django.db import migrations, models
from ComSemApp.utils import transcribe_and_get_length_audio_file


def delete_attempts_without_audio(apps, schema_editor):
    speakingpracticeattempt = apps.get_model('ComSemApp','SpeakingPracticeAttempt')
    db_alias = schema_editor.connection.alias
    attempts : models.QuerySet[ComSemApp.models.SpeakingPracticeAttempt] = speakingpracticeattempt.objects.using(db_alias).filter(models.Q(audio__isnull=True) | models.Q(audio__exact=''))
    attempts.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('ComSemApp', '0024_speakingpracticeattempt_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='speakingpracticeattempt',
            name='transcription',
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.RunPython(delete_attempts_without_audio, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='speakingpracticeattempt',
            name='audio',
            field=models.FileField(upload_to=ComSemApp.models.speaking_practice_audio_directory),
        ),
        migrations.AlterField(
            model_name='speakingpracticeattempt',
            name='correct',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Correctness Score'),
        ),
        migrations.AlterField(
            model_name='speakingpracticeattempt',
            name='wpm',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Words per Minute'),
        ),
    ]
