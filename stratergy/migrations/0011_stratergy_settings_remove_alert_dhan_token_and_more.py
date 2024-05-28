# Generated by Django 4.2.8 on 2024-01-01 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stratergy', '0010_executed_stratergy_url_alter_alert_symbol_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stratergy_settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='https://smart-algo.in/alert/smartorder', max_length=150)),
                ('upstox_access_token', models.CharField(default='', max_length=5000)),
            ],
        ),
        migrations.RemoveField(
            model_name='alert',
            name='dhan_token',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='instrument_type',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='segment',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='upstox_access_token',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='url',
        ),
        migrations.AddField(
            model_name='alert',
            name='current_volume',
            field=models.PositiveIntegerField(default=5000000000000),
        ),
    ]