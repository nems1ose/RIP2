# Generated by Django 4.2.7 on 2024-11-12 21:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_filmstatus_alter_history_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 12, 21, 54, 23, 738951, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]
