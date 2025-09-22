# Generated migration for Todo model
from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When the record was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='When the record was last updated')),
                ('title', models.CharField(help_text='Short title for the todo', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Optional longer description')),
                ('is_completed', models.BooleanField(default=False, help_text='Completion status')),
                ('due_date', models.DateTimeField(blank=True, help_text='Optional due date/time', null=True)),
                ('owner', models.ForeignKey(help_text='User who owns this todo', on_delete=django.db.models.deletion.CASCADE, related_name='todos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='todo',
            index=models.Index(fields=['owner', 'is_completed'], name='api_todo_owner_iscomp_idx'),
        ),
    ]
