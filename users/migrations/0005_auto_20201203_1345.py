# Generated by Django 3.1.4 on 2020-12-03 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20201121_0810'),
        ('shop', '0001_initial'),
        ('users', '0004_auto_20201121_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shops',
            field=models.ManyToManyField(blank=True, related_name='OwnedShops', to='shop.Shop'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cart',
            field=models.ManyToManyField(blank=True, related_name='Cart', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='user',
            name='parchases',
            field=models.ManyToManyField(blank=True, related_name='Purchases', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='user',
            name='wishList',
            field=models.ManyToManyField(blank=True, related_name='WishList', to='products.Product'),
        ),
    ]