# Generated by Django 4.1.1 on 2022-09-20 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CourierCompany",
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
                ("company_name", models.CharField(max_length=50)),
                (
                    "company_logo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="logos",
                        verbose_name="Upload Company logo.",
                    ),
                ),
                ("company_phone_number", models.CharField(max_length=50)),
                ("company_email", models.EmailField(max_length=64)),
                ("address", models.CharField(max_length=100)),
                (
                    "all1zed_commission",
                    models.FloatField(
                        default=5.0,
                        help_text="Commission charged per Package Sent (In Zambian Kwacha)",
                    ),
                ),
                (
                    "number_of_packages",
                    models.IntegerField(
                        default=0, help_text="Initial number of packages."
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Login Username",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Courier Companies",},
        ),
    ]
