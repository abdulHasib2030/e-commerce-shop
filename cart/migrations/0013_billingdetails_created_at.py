# Generated by Django 5.0.4 on 2024-04-18 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingdetails',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]