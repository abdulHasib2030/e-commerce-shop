# Generated by Django 5.0.4 on 2024-04-11 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('sellerAccount', '0006_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sellerAccount.selleraccount'),
        ),
    ]
