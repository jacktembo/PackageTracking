# Generated by Django 4.1.1 on 2022-09-21 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0002_couriercompany_company_initials_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="package",
            name="tracking_number",
            field=models.CharField(
                default="416862772595", editable=False, max_length=255
            ),
        ),
    ]
