# Generated by Django 5.0.4 on 2024-04-10 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_billingdetails_user'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingdetails',
            name='cart_item',
        ),
        migrations.AddField(
            model_name='billingdetails',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='billingdetails',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
