# Generated by Django 3.1.5 on 2021-05-15 16:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_auto_20210515_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='time',
            field=models.TimeField(default=datetime.time(16, 19, 0, 802603)),
        ),
    ]