# Generated by Django 4.2.7 on 2024-03-14 17:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stratergy', '0022_stratergy_settings_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='executed_stratergy',
            name='symbol',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='executed_stratergy',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 22, 57, 51, 224473), primary_key=True, serialize=False),
        ),
    ]
