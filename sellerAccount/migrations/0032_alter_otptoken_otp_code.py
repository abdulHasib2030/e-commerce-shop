# Generated by Django 5.0.4 on 2024-04-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerAccount', '0031_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='49ddb8', max_length=10),
        ),
    ]
