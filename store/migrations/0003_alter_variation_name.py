# Generated by Django 5.1 on 2024-10-12 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='name',
            field=models.CharField(choices=[('Color', 'color'), ('Size', 'size')], max_length=100),
        ),
    ]