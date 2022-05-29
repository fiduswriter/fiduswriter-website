from django.db import models
from django.conf import settings

from document.models import Document


STATUS_CHOICES = (
    ("unsubmitted", "Unsubmitted"),
    ("submitted", "Submitted"),
    ("published", "Published"),
    ("resubmitted", "Resubmitted"),
)


class Publication(models.Model):
    document = models.OneToOneField(
        Document, on_delete=models.deletion.CASCADE
    )
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.deletion.CASCADE,
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=11, default="unsubmitted"
    )
    message_to_editor = models.TextField(default="")


class Editor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.deletion.CASCADE,
    )
