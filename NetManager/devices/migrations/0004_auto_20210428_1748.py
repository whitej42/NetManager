# Generated by Django 3.1.5 on 2021-04-28 16:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20210428_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='time',
            field=models.TimeField(default=datetime.time(16, 48, 33, 143949)),
        ),
        migrations.AlterField(
            model_name='backup',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
