# Generated by Django 5.1 on 2024-12-10 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_brand_gender_variationtype_remove_product_stock_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
    ]