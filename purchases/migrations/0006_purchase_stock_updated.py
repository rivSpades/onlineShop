# Generated by Django 5.1 on 2024-12-10 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0005_alter_purchase_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='stock_updated',
            field=models.BooleanField(default=False),
        ),
    ]