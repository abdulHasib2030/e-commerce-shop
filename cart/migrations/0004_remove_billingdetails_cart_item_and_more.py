# Generated by Django 5.0.4 on 2024-04-10 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_billingdetails_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingdetails',
            name='cart_item',
        ),
        migrations.AddField(
            model_name='billingdetails',
            name='cart_item',
            field=models.ManyToManyField(to='cart.cartitem'),
        ),
    ]
