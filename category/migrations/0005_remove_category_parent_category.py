# Generated by Django 5.1 on 2024-10-25 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_maincategory_options_category_parent_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_category',
        ),
    ]