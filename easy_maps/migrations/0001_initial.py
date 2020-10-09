# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("address", models.CharField(unique=True, max_length=255, verbose_name="address")),
                (
                    "computed_address",
                    models.CharField(max_length=255, null=True, verbose_name="computed address", blank=True),
                ),
                ("latitude", models.FloatField(null=True, verbose_name="latitude", blank=True)),
                ("longitude", models.FloatField(null=True, verbose_name="longitude", blank=True)),
                ("geocode_error", models.BooleanField(default=False, verbose_name="geocode error")),
            ],
            options={
                "verbose_name": "EasyMaps Address",
                "verbose_name_plural": "Address Geocoding Cache",
            },
        ),
    ]
