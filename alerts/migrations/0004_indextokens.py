# Generated by Django 4.2.5 on 2023-12-05 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0003_alter_orders_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BANKNIFTY', models.CharField(max_length=100)),
                ('CRUDEOIL', models.CharField(max_length=100)),
                ('SENSEX', models.CharField(max_length=100)),
                ('NIFTY', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Index Token Number',
                'verbose_name_plural': 'Index Tokens',
            },
        ),
    ]
