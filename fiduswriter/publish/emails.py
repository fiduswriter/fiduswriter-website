from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import escape
from django.utils.translation import gettext as _

from base.html_email import html_email


def send_submit_notification(
    document_title,
    link,
    message,
    editor_name,
    editor_email,
):

    if len(document_title) == 0:
        document_title = _("Untitled")
    message_text = _(
        (
            f"Hey {editor_name}, the document '{document_title}' has "
            "been submitted to be published. You or another editor need to "
            "approve it before it will be made accessible to the general "
            "public."
            f"\nOpen the document: {link}"
        )
    )
    body_html_intro = _(
        (
            f"<p>Hey {escape(editor_name)}<br>the document '{escape(document_title)}' has "
            "been submitted to be published. You or another editor need to "
            "approve it before it will be made accessible to the general "
            "public.</p>"
        )
    )
    if len(message):
        message_text += _(f"Message from the author: {message}")
        body_html_intro += _(
            f"<p>Message from the author: {escape(message)}</p>"
        )
    review_document_str = _(f"Review {escape(document_title)}")
    access_the_document_str = _("Access the Document")
    document_str = _("Document")
    body_html = (
        f"<h1>{review_document_str}</h1>"
        f"{body_html_intro}"
        "<table>"
        f"<tr><td>{document_str}</td><td>"
        f"<b>{document_title}</b>"
        "</td></tr>"
        "</table>"
        f'<div class="actions"><a class="button" href="{link}">'
        f"{access_the_document_str}"
        "</a></div>"
    )
    send_mail(
        _(f"Document shared: {escape(document_title)}"),
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        [editor_email],
        fail_silently=True,
        html_message=html_email(body_html),
    )
