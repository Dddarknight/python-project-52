# Generated by Django 4.1 on 2022-09-05 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0005_alter_tasks_executor_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labels',
            name='task',
            field=models.ManyToManyField(
                related_name='labels', to='task_manager.tasks'),
        ),
    ]
