from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from document.models import Document, AccessRight

from . import models


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
            document=document, user=request.user
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    message_to_editor = request.POST.get("message_to_editor")
    publication, created = models.Publication.objects.select_related(
        "document"
    ).get_or_create(
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
    return JsonResponse(response, status=status)
