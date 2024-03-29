# Generated by Django 4.0.4 on 2022-04-28 03:52

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_contactus'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('short', models.CharField(max_length=600)),
                ('desc', ckeditor.fields.RichTextField()),
                ('img', models.ImageField(upload_to='aboutus/')),
            ],
        ),
    ]
