# Generated by Django 3.1.3 on 2021-01-06 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_user_last_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_activity',
        ),
    ]
