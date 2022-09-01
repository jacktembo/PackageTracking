# Generated by Django 4.1 on 2022-09-01 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("global", "0017_remove_vehicle_user_alter_package_tracking_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="package",
            name="tracking_number",
            field=models.CharField(
                default="4826983243", editable=False, max_length=255, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="vehicle", name="departure_time", field=models.TimeField(),
        ),
    ]
