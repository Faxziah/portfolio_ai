# Generated migration based on current models

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AIChatLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('user_message', models.TextField()),
                ('ai_response', models.TextField()),
                ('system_prompt', models.TextField(blank=True)),
                ('resume_included', models.BooleanField(default=False)),
                ('resume_content', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'verbose_name': 'AI Chat Log',
                'verbose_name_plural': 'AI Chat Logs',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ResumeMarkdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, help_text='Upload your resume in Markdown (.md) format. Maximum 10,000 words.', upload_to='resumes/')),
                ('content', models.TextField(editable=False, help_text='Content extracted from uploaded file')),
                ('uploaded_at', models.DateTimeField(auto_now=True)),
                ('word_count', models.IntegerField(default=0, editable=False)),
            ],
            options={
                'verbose_name': 'Upload Resume',
                'verbose_name_plural': 'Upload Resume',
            },
        ),
    ]

