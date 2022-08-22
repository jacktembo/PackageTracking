# Generated by Django 4.1 on 2022-08-22 14:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("global", "0014_couriercompany_account_balance_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="couriercompany", name="account_balance",),
        migrations.AddField(
            model_name="couriercompany",
            name="number_of_packages",
            field=models.IntegerField(
                default=0, help_text="Initial number of packages."
            ),
        ),
        migrations.AlterField(
            model_name="package",
            name="tracking_number",
            field=models.CharField(
                default="1907028190", editable=False, max_length=255, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="departure_time",
            field=models.TimeField(default=datetime.time(16, 16, 51, 79732)),
        ),
    ]
