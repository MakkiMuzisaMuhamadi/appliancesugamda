# Generated by Django 5.0.2 on 2024-03-06 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0024_remove_orderitem_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyNow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('product_name', models.CharField(max_length=255)),
                ('product_price', models.DecimalField(decimal_places=2, default='', max_digits=10)),
                ('product_id', models.CharField(max_length=255)),
                ('product_category', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
