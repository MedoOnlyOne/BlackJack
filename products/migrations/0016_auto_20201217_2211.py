# Generated by Django 3.1.3 on 2020-12-17 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20201217_2211'),
        ('products', '0015_auto_20201217_2211'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]