# Generated by Django 5.0.2 on 2024-03-03 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0012_filteredbrand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.DeleteModel(
            name='FilteredBrand',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
