# Generated by Django 4.1.1 on 2022-11-11 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("general", "0005_alter_package_package_value_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PendingPaymentApproval",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("session_uuid", models.CharField(max_length=255)),
                ("product_id", models.CharField(max_length=255)),
                ("date_time_created", models.DateTimeField(auto_now_add=True)),
                ("phone_number", models.CharField(max_length=255)),
                ("reference_number", models.CharField(max_length=255)),
                ("amount", models.FloatField()),
                ("plan_id", models.IntegerField()),
                (
                    "courier_company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="general.couriercompany",
                    ),
                ),
            ],
        ),
    ]