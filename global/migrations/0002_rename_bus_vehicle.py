# Generated by Django 4.1 on 2022-08-11 11:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("global", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="Bus", new_name="Vehicle",),
    ]
