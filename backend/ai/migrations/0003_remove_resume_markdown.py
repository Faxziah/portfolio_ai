# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0002_alter_resumemarkdown_file'),
    ]

    operations = [
        # Delete ResumeMarkdown model
        migrations.DeleteModel(
            name='ResumeMarkdown',
        ),
        # Remove old fields from AIChatLog
        migrations.RemoveField(
            model_name='aichatlog',
            name='system_prompt',
        ),
        migrations.RemoveField(
            model_name='aichatlog',
            name='resume_included',
        ),
        migrations.RemoveField(
            model_name='aichatlog',
            name='resume_content',
        ),
        # Add language field to AIChatLog
        migrations.AddField(
            model_name='aichatlog',
            name='language',
            field=models.CharField(max_length=10, default='en'),
        ),
    ]
