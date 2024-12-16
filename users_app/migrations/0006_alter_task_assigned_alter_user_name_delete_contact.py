# Generated by Django 5.1.3 on 2024-12-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts_app', '0001_initial'),
        ('users_app', '0005_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned',
            field=models.ManyToManyField(blank=True, to='contacts_app.contact'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(help_text='Max 20 characters', max_length=20),
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
