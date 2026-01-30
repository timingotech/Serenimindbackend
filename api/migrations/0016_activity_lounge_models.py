# Generated manually for Activity Lounge models

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_chatthread_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('external_url', models.URLField(blank=True)),
                ('moods', models.CharField(max_length=255, help_text='Comma-separated mood tags')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('play_url', models.URLField(blank=True)),
                (
                    'moods',
                    models.CharField(
                        max_length=255,
                        help_text='Comma-separated mood or category tags',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ActivityExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('exercise_type', models.CharField(max_length=100, blank=True)),
                ('reason', models.TextField(blank=True)),
                ('gif_url', models.URLField(blank=True)),
                ('moods', models.CharField(max_length=255, help_text='Comma-separated mood tags')),
            ],
        ),
        migrations.CreateModel(
            name='ActivitySound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=100, blank=True)),
                ('duration', models.CharField(max_length=20, blank=True)),
                ('audio_url', models.URLField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('moods', models.CharField(max_length=255, help_text='Comma-separated mood tags')),
            ],
        ),
    ]
