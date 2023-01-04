# Generated by Django 3.2.13 on 2022-07-15 11:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_auto_20220715_1044"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="added",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="publication",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
