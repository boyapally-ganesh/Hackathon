# Generated by Django 5.1.1 on 2024-09-05 18:52

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HackathonModels',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='hackthons/backgrounds/')),
                ('hackathon_image', models.ImageField(blank=True, null=True, upload_to='hackthons/')),
                ('submissions_type', models.CharField(choices=[('image', 'image'), ('file', 'File'), ('link', 'Link')], max_length=10)),
                ('start_datetime', models.DateTimeField()),
                ('end_dateTime', models.DateTimeField()),
                ('reward_prize', models.CharField(max_length=255)),
                ('authorized', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start_datetime'],
            },
        ),
        migrations.CreateModel(
            name='RegistrationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='app.hackathonmodels')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('submission_name', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('submission_image', models.ImageField(blank=True, null=True, upload_to='submissions/images/')),
                ('submission_file', models.FileField(blank=True, null=True, upload_to='submission/files/')),
                ('submission_link', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='app.hackathonmodels')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
