# Generated by Django 4.1 on 2022-09-13 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0025_alter_package_tracking_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="package",
            name="tracking_number",
            field=models.CharField(
                default="3272516202", editable=False, max_length=255, unique=True
            ),
        ),
    ]
