# Generated by Django 5.0.4 on 2024-04-18 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_billingdetails_sub_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingdetails',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
