# Generated by Django 3.1.4 on 2020-12-24 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
        ('users', '0016_auto_20201217_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='shops',
        ),
        migrations.AddField(
            model_name='user',
            name='shop',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.shop'),
        ),
    ]
