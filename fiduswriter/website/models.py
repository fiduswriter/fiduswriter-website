from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site

from document.models import Document


STATUS_CHOICES = (
    ("unsubmitted", "Unsubmitted"),
    ("submitted", "Submitted"),
    ("published", "Published"),
    ("resubmitted", "Resubmitted"),
)


class Publication(models.Model):
    document = models.OneToOneField(
        Document,
        on_delete=models.deletion.CASCADE,
    )
    title = models.CharField(max_length=255, default="", blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.deletion.CASCADE,
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=11,
        default="unsubmitted",
    )
    messages = models.JSONField(default=list)
    authors = models.JSONField(default=list)
    keywords = models.JSONField(default=list)
    abstract = models.TextField(default="")

    html_src = models.TextField(
        default="",
    )  # The original HTML as exported from the frontend
    html_output = models.TextField(
        default="",
    )  # The HTML with asset locations replaced.

    def __str__(self):
        return f"{self.title} ({self.document_id}, {self.status})"


def publication_asset_location(instance, filename):
    # preserve the original filename
    instance.filename = filename
    return "/".join(["publication_assets", filename])


class PublicationAsset(models.Model):
    publication = models.ForeignKey(
        Publication,
        on_delete=models.deletion.CASCADE,
    )
    file = models.FileField(
        upload_to=publication_asset_location,
        help_text=(
            "A file references in the HTML of a Publication. The filepath "
            "will be replaced with the final url of the file in the style."
        ),
    )
    filepath = models.CharField(
        max_length=255,
        help_text="The original filepath.",
    )


default_style = """
:root {
    --posts_per_page: 10; /* Number of posts per page on frontpage. Disable for all. */
}
"""


class Design(models.Model):
    site = models.OneToOneField(Site, on_delete=models.deletion.CASCADE)
    style = models.TextField(
        help_text="The CSS style definiton.", default=default_style
    )

    def __str__(self):
        return f"{self.site.name}"


class Editor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.deletion.CASCADE,
        related_name="website_editor",
    )

    def __str__(self):
        return f"Editor {self.user.username}"
