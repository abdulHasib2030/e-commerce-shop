# Generated by Django 5.0.4 on 2024-04-14 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_size_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.IntegerField(null=True),
        ),
    ]
