# Generated by Django 4.0.4 on 2022-05-05 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_aboutus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='gender',
        ),
    ]
