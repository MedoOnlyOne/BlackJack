# Generated by Django 3.1.3 on 2020-11-21 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201121_1146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='wishListt',
            new_name='wishList',
        ),
    ]
