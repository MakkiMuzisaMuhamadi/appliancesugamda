# Generated by Django 5.0.2 on 2024-03-05 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0023_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
    ]
