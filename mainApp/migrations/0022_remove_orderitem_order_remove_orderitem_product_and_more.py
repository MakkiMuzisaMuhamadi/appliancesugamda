# Generated by Django 5.0.2 on 2024-03-05 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0021_remove_order_address_remove_order_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
