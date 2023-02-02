# Generated by Django 3.2.13 on 2022-05-27 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("document", "0018_fidus_3_4"),
    ]

    operations = [
        migrations.CreateModel(
            name="Publication",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("unsubmitted", "Unsubmitted"),
                            ("submitted", "Submitted"),
                            ("published", "Published"),
                            ("resubmitted", "Resubmitted"),
                        ],
                        default="unsubmitted",
                        max_length=11,
                    ),
                ),
                ("message_to_editor", models.TextField(default="")),
                (
                    "document",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="document.document",
                    ),
                ),
                (
                    "submitter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Editor",
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
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
