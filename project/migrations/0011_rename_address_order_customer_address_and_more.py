# Generated by Django 4.0.3 on 2022-04-09 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_order_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='customer_address',
        ),
        migrations.AddField(
            model_name='order',
            name='customer_email',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_mobile',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
