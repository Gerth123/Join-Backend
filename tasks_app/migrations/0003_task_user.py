# Generated by Django 5.1.3 on 2024-12-22 23:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0002_task_status'),
        ('users_app', '0003_remove_task_subtasks_remove_task_assigned_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(default=28, on_delete=django.db.models.deletion.CASCADE, to='users_app.userprofile'),
            preserve_default=False,
        ),
    ]
