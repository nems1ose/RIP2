# Generated by Django 4.2.7 on 2024-11-02 17:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_film_filmhistory_history_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 2, 17, 12, 11, 84963, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]