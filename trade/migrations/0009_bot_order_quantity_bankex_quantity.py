# Generated by Django 4.2.8 on 2024-02-23 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0008_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot_order_quantity',
            name='bankex_quantity',
            field=models.PositiveIntegerField(blank=True, default=40, null=True),
        ),
    ]
