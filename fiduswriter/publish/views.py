from django.http import HttpResponse, JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType

from document.models import Document, AccessRight

from . import models, emails


@login_required
@require_POST
def get_doc_info(request):
    response = {}
    document_id = int(request.POST.get("doc_id"))
    document = Document.objects.filter(id=document_id).first()
    if not document:
        return HttpResponse("Not found", status=404)
    if (
        document.owner != request.user
        and not AccessRight.objects.filter(
            document=document, user=request.user
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    response["submission"] = dict()
    publication = models.Publication.objects.filter(
        document_id=document_id,
    ).first()
    if publication:
        response["submission"]["status"] = publication.status
        response["submission"][
            "message_to_editor"
        ] = publication.message_to_editor
    else:
        response["submission"]["status"] = "unsubmitted"
        response["submission"]["message_to_editor"] = ""
    if models.Editor.objects.filter(user_id=request.user.id):
        user_role = "editor"
    else:
        user_role = "author"
    response["submission"]["user_role"] = user_role
    status = 200
    return JsonResponse(response, status=status)


@login_required
@require_POST
def submit_doc(request):
    response = {}
    document_id = int(request.POST.get("doc_id"))
    status = 200
    document = Document.objects.filter(id=document_id).first()
    if not document:
        return HttpResponse("Not found", status=404)
    if (
        document.owner != request.user
        and not AccessRight.objects.filter(
            document=document, user=request.user, right="write"
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    message_to_editor = request.POST.get("message_to_editor")
    publication, created = models.Publication.objects.get_or_create(
        document_id=document_id,
        defaults={
            "submitter": request.user,
            "status": "submitted",
            "message_to_editor": message_to_editor,
        },
    )
    if not created:
        publication.message_to_editor = message_to_editor
        if publication.status in ["published", "resubmitted"]:
            publication.status = "resubmitted"
        else:
            publication.status = "submitted"
        publication.save()
    link = HttpRequest.build_absolute_uri(request, document.get_absolute_url())
    user_ct = ContentType.objects.get(app_label="user", model="user")
    for editor in models.Editor.objects.select_related("user").all():
        if editor.user == document.owner or request.user == editor.user:
            continue
        access_right, created = AccessRight.objects.get_or_create(
            document_id=document_id,
            holder_id=editor.user.id,
            holder_type=user_ct,
            defaults={
                "rights": "write",
            },
        )
        if not created and access_right.rights != "write":
            access_right.rights = "write"
            access_right.save()
        emails.send_submit_notification(
            document.title, link, editor.user.readable_name, editor.user.email
        )

    response["status"] = publication.status
    return JsonResponse(response, status=status)


@login_required
@require_POST
def reject_doc(request):
    response = {}
    editor = models.Editor.objects.filter(user=request.user).first()
    if not editor:
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    document_id = int(request.POST.get("doc_id"))
    status = 200
    document = Document.objects.filter(id=document_id).first()
    if not document:
        return HttpResponse("Not found", status=404)
    if (
        document.owner != request.user
        and not AccessRight.objects.filter(
            document=document, user=request.user
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    publication = models.Publication.objects.filter(
        document_id=document.id
    ).first()
    if publication:
        publication.delete()
    return JsonResponse(response, status=status)


@login_required
@require_POST
def publish_doc(request):
    response = {}
    editor = models.Editor.objects.filter(user=request.user).first()
    if not editor:
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    document_id = int(request.POST.get("doc_id"))
    status = 200
    publication = (
        models.Publication.objects.select_related("document")
        .filter(document_id=document_id)
        .first()
    )
    if not publication:
        return HttpResponse("Not found", status=404)
    if (
        publication.document.owner != request.user
        and not AccessRight.objects.filter(
            document=publication.document, user=request.user
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    publication.status = "published"
    publication.message_to_editor = ""
    publication.save()
    return JsonResponse(response, status=status)
