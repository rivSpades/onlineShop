# Generated by Django 5.1 on 2024-10-25 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('banner_img', models.ImageField(upload_to='images/banners/')),
                ('discount', models.CharField(max_length=3)),
                ('black_friday', models.BooleanField(default=False)),
            ],
        ),
    ]