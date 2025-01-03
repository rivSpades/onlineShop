# Generated by Django 5.1 on 2024-12-10 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseproduct',
            name='total_price',
        ),
        migrations.AddField(
            model_name='purchase',
            name='extra_costs',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='total_amount',
            field=models.FloatField(default=0.0),
        ),
    ]
