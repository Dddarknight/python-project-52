# Generated by Django 4.1 on 2022-09-04 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_statuses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('description', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='author',
                    to=settings.AUTH_USER_MODEL)),
                ('executor', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='executor',
                    to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to='task_manager.statuses')),
            ],
        ),
    ]
