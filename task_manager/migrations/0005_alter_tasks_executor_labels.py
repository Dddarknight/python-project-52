# Generated by Django 4.1 on 2022-09-05 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0004_alter_tasks_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='executor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='executor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('task', models.ManyToManyField(to='task_manager.tasks')),
            ],
        ),
    ]
