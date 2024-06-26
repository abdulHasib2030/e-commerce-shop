# Generated by Django 5.0.4 on 2024-04-10 03:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('town_city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('zipcode', models.IntegerField()),
                ('mobile', models.IntegerField(max_length=11)),
                ('email_address', models.EmailField(max_length=254)),
                ('note', models.TextField(max_length=500)),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cartitem')),
            ],
        ),
    ]
