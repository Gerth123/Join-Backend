# Generated by Django 5.1.3 on 2024-12-23 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0004_auto_20241223_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
