# Generated by Django 4.2.7 on 2024-11-07 10:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_history_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 7, 10, 14, 39, 987410, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]
