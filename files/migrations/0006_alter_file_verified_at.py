# Generated by Django 3.2.13 on 2022-06-10 05:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_rename_veriried_at_file_verified_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='verified_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
