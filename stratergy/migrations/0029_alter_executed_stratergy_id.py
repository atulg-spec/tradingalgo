# Generated by Django 4.2.7 on 2024-03-18 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stratergy', '0028_alter_executed_stratergy_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executed_stratergy',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
