# Generated by Django 5.0.4 on 2024-04-14 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerAccount', '0012_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='d298f6', max_length=10),
        ),
    ]