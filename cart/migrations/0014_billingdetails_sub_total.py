# Generated by Django 5.0.4 on 2024-04-18 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_billingdetails_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingdetails',
            name='sub_total',
            field=models.IntegerField(null=True),
        ),
    ]