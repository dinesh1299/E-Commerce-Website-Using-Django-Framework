# Generated by Django 4.0.3 on 2022-04-02 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_orderitem_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]