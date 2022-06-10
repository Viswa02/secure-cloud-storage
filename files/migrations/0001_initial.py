# Generated by Django 3.2.13 on 2022-06-04 03:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('blob_name', models.CharField(max_length=150)),
                ('size', models.IntegerField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('integrity_score', models.FloatField(default=100)),
                ('integrity', models.BooleanField(default=True)),
            ],
        ),
    ]
