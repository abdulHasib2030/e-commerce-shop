# Generated by Django 5.0.4 on 2024-04-11 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerAccount', '0005_otptoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='3ff305', max_length=10),
        ),
    ]
