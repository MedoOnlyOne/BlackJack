# Generated by Django 3.1.5 on 2021-01-09 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_product_vistits'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='vistits',
            new_name='visits',
        ),
    ]