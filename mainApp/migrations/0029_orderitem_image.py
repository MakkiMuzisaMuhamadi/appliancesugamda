# Generated by Django 5.0.2 on 2024-03-09 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0028_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='image',
            field=models.ImageField(default='', upload_to='orders/'),
        ),
    ]
