# Generated by Django 5.0.2 on 2024-03-06 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0026_buynow2_delete_buynow'),
    ]

    operations = [
        migrations.AddField(
            model_name='buynow2',
            name='product_brand',
            field=models.CharField(default='', max_length=255),
        ),
    ]