# Generated by Django 4.1.2 on 2023-02-15 10:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0009_design"),
    ]

    operations = [
        migrations.AlterField(
            model_name="publication",
            name="status",
            field=models.CharField(
                choices=[
                    ("unsubmitted", "Unsubmitted"),
                    ("submitted", "Submitted"),
                    ("published", "Published"),
                    ("rejected", "Rejected"),
                    ("resubmitted", "Resubmitted"),
                ],
                default="unsubmitted",
                max_length=11,
            ),
        ),
    ]