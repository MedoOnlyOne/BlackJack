# Generated by Django 3.1.3 on 2020-12-17 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20201217_2055'),
        ('users', '0014_auto_20201217_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cart',
        ),
        migrations.AddField(
            model_name='user',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.cart'),
        ),
        migrations.RemoveField(
            model_name='user',
            name='wishlist',
        ),
        migrations.AddField(
            model_name='user',
            name='wishlist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.wishlist'),
        ),
    ]
