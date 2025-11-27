# Generated manually for RAG cleanup

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rag', '0002_aichatlog'),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS rag_resume_chunk CASCADE;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

