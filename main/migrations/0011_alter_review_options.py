# Generated by Django 4.0.4 on 2022-05-04 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_review_create_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-create_at',)},
        ),
    ]
