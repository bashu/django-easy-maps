# Generated by Django 2.1.7 on 2019-03-29 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_maps', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='geocode_error',
        ),
        migrations.AddField(
            model_name='address',
            name='exception',
            field=models.TextField(blank=True, verbose_name='has exception?'),
        ),
    ]
