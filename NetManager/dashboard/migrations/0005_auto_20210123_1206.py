# Generated by Django 3.1.5 on 2021-01-23 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20201208_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='id',
        ),
        migrations.AlterField(
            model_name='device',
            name='device',
            field=models.CharField(max_length=250, primary_key=True, serialize=False),
        ),
    ]
