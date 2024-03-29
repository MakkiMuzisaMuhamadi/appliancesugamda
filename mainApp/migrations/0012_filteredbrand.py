# Generated by Django 5.0.2 on 2024-03-03 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0011_remove_product_description_remove_product_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilteredBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.category')),
            ],
        ),
    ]
