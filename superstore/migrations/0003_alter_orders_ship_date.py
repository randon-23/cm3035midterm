# Generated by Django 5.0 on 2023-12-21 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superstore', '0002_alter_addresses_address_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='ship_date',
            field=models.DateField(null=True),
        ),
    ]