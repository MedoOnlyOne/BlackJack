# Generated by Django 3.1.4 on 2020-12-27 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20201227_2102'),
        ('users', '0021_auto_20201227_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='orders',
            field=models.ManyToManyField(blank=True, related_name='orders', to='users.Order'),
        ),
        migrations.AlterField(
            model_name='user',
            name='shop',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.shop'),
        ),
    ]