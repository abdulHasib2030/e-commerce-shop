# Generated by Django 5.0.4 on 2024-04-14 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerAccount', '0013_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='f59d8b', max_length=10),
        ),
    ]
