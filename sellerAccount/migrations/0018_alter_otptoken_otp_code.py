# Generated by Django 5.0.4 on 2024-04-15 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerAccount', '0017_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='21916e', max_length=10),
        ),
    ]
