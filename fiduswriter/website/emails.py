from base.html_email import html_email
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import escape
from django.utils.translation import gettext as _


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
        f"Hey {editor_name}, the document '{document_title}' has "
        "been submitted to be published. You or another editor need to "
        "approve it before it will be made accessible to the general "
        "public."
        f"\nOpen the document: {link}",
    )
    body_html_intro = _(
        f"<p>Hey {escape(editor_name)}<br>the document '{escape(document_title)}' has "
        "been submitted to be published. You or another editor need to "
        "approve it before it will be made accessible to the general "
        "public.</p>",
    )
    if len(message):
        message_text += _(f"\nMessage from the author: {message}")
        body_html_intro += _(
            f"<p>Message from the author: {escape(message)}</p>",
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


def send_review_notification(
    document_title,
    link,
    message,
    author_name,
    author_email,
):

    if len(document_title) == 0:
        document_title = _("Untitled")
    message_text = _(
        f"Hey {author_name}, the document '{document_title}' has "
        "been reviewed. You or another author need to change some things "
        "before it can be published. Please resubmit it once you are done. "
        f"\nOpen the document: {link}",
    )
    body_html_intro = _(
        f"<p>Hey {escape(author_name)}<br>the document '{escape(document_title)}' has "
        "been reviewed. You or another author need to change some things "
        "before it can be published. Please resubmit it once you are done.</p>",
    )
    if len(message):
        message_text += _(f"\nMessage from the editor: {message}")
        body_html_intro += _(
            f"<p>Message from the editor: {escape(message)}</p>",
        )
    review_document_str = _(f"{escape(document_title)} reviewed")
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
        _(f"Document: {escape(document_title)}"),
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        [author_email],
        fail_silently=True,
        html_message=html_email(body_html),
    )


def send_reject_notification(
    document_title,
    link,
    message,
    author_name,
    author_email,
):

    if len(document_title) == 0:
        document_title = _("Untitled")
    message_text = _(
        f"Hey {author_name}, the document '{document_title}' has "
        "been reviewed and rejected. "
        f"\nOpen the document: {link}",
    )
    body_html_intro = _(
        f"<p>Hey {escape(author_name)}<br>the document '{escape(document_title)}' has "
        "been reviewed and rejected.</p>",
    )
    if len(message):
        message_text += _(f"\nMessage from the editor: {message}")
        body_html_intro += _(
            f"<p>Message from the editor: {escape(message)}</p>",
        )
    review_document_str = _(f"{escape(document_title)} rejected")
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
        _(f"Document: {escape(document_title)}"),
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        [author_email],
        fail_silently=True,
        html_message=html_email(body_html),
    )


def send_publish_notification(
    document_title,
    link,
    message,
    author_name,
    author_email,
):

    if len(document_title) == 0:
        document_title = _("Untitled")
    message_text = _(
        f"Hey {author_name}, the document '{document_title}' has "
        "been reviewed and published. "
        f"\nOpen the document: {link}",
    )
    body_html_intro = _(
        f"<p>Hey {escape(author_name)}<br>the document '{escape(document_title)}' has "
        "been reviewed and published.</p>",
    )
    if len(message):
        message_text += _(f"\nMessage from the editor: {message}")
        body_html_intro += _(
            f"<p>Message from the editor: {escape(message)}</p>",
        )
    review_document_str = _(f"{escape(document_title)} published")
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
        _(f"Document: {escape(document_title)}"),
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        [author_email],
        fail_silently=True,
        html_message=html_email(body_html),
    )
