# Generated by Django 3.1.4 on 2020-12-27 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20201224_1451'),
        ('users', '0018_auto_20201224_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_delivered', models.BooleanField(default=False)),
                ('products', models.ManyToManyField(related_name='ordered_products', to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='orders',
            field=models.ManyToManyField(related_name='orders', to='users.Order'),
        ),
    ]