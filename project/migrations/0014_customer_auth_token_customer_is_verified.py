# Generated by Django 4.0.3 on 2022-04-10 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_remove_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='auth_token',
            field=models.CharField(default='a', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
