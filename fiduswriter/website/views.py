import time
import zipfile

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from document.models import AccessRight
from document.models import Document
from django.core.paginator import Paginator

from . import emails
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
            document=document,
            user=request.user,
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    response["submission"] = {}
    publication = models.Publication.objects.filter(
        document_id=document_id,
    ).first()
    if publication:
        response["submission"]["status"] = publication.status
        response["submission"]["messages"] = publication.messages
    else:
        response["submission"]["status"] = "unsubmitted"
        response["submission"]["messages"] = []
    if request.user.has_perm(
        "website.add_publication",
    ) or models.Editor.objects.filter(
        user_id=request.user.id,
    ):
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
            document=document,
            user=request.user,
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing document access rights", status=403)
    publication, created = models.Publication.objects.get_or_create(
        document_id=document_id,
        defaults={"submitter": request.user, "status": "submitted"},
    )
    if (
        publication.status == "published"
        and not created
        and request.user.has_perm("website.change_publication")
    ):
        # The user has permission to publish the document immediately.
        publication.title = request.POST.get("title")
        publication.abstract = request.POST.get("abstract")
        publication.authors = request.POST.getlist("authors[]")
        publication.keywords = request.POST.getlist("keywords[]")
        # Delete all existing assets
        models.PublicationAsset.objects.filter(
            publication=publication,
        ).delete()
        html_zip = zipfile.ZipFile(request.FILES.get("html.zip"))
        body_html = html_zip.open("document.html").read().decode("utf-8")
        publication.html_src = body_html
        publication.status = "published"
        message = {
            "type": "publish",
            "message": request.POST.get("message"),
            "user": request.user.readable_name,
            "time": time.time(),
        }
        publication.messages.append(message)
        response["message"] = message
        publication.save()
        response["status"] = publication.status
        return JsonResponse(response, status=status)
    message = {
        "type": "submit",
        "message": request.POST.get("message"),
        "user": request.user.readable_name,
        "time": time.time(),
    }
    publication.messages.append(message)
    response["message"] = message
    if not created:
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
        if editor.user != request.user:
            emails.send_submit_notification(
                document.title,
                link,
                request.POST.get("message"),
                editor.user.readable_name,
                editor.user.email,
            )

    response["status"] = publication.status
    return JsonResponse(response, status=status)


@login_required
@require_POST
def reject_doc(request):
    response = {}
    if not (
        request.user.has_perm("website.add_publication")
        or request.user.has_perm("website.change_publication")
        or models.Editor.objects.filter(user=request.user).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    document_id = int(request.POST.get("doc_id"))
    document = Document.objects.filter(id=document_id).first()
    if not document:
        return HttpResponse("Not found", status=404)
    if (
        document.owner != request.user
        and not AccessRight.objects.filter(
            document=document,
            user=request.user,
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing document access rights", status=403)
    status = 200
    if (
        request.user.has_perm("website.add_publication")
        or models.Editor.objects.filter(user=request.user).first()
    ):
        publication, created = models.Publication.objects.get_or_create(
            document_id=document_id,
            defaults={"submitter": request.user, "status": "rejected"},
        )
    else:
        publication = models.Publication.objects.filter(
            document_id=document_id,
        ).first()
        if not publication:
            # Access forbidden
            return HttpResponse("Missing document access rights", status=403)
        created = False
    if not created:
        publication.status = "rejected"
    message = {
        "type": "reject",
        "message": request.POST.get("message"),
        "user": request.user.readable_name,
        "time": time.time(),
    }
    publication.messages.append(message)
    publication.save()
    response["message"] = message
    response["status"] = publication.status
    if document.owner != request.user:
        emails.send_reject_notification(
            document.title,
            HttpRequest.build_absolute_uri(
                request, document.get_absolute_url()
            ),
            request.POST.get("message"),
            document.owner.readable_name,
            document.owner.email,
        )
    return JsonResponse(response, status=status)


@login_required
@require_POST
def review_doc(request):
    response = {}
    if not (
        request.user.has_perm("website.add_publication")
        or request.user.has_perm("website.change_publication")
        or models.Editor.objects.filter(user=request.user).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    document_id = int(request.POST.get("doc_id"))
    document = Document.objects.filter(id=document_id).first()
    if not document:
        return HttpResponse("Not found", status=404)
    if (
        document.owner != request.user
        and not AccessRight.objects.filter(
            document=document,
            user=request.user,
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    status = 200
    if (
        request.user.has_perm("website.add_publication")
        or models.Editor.objects.filter(user=request.user).first()
    ):
        publication, _created = models.Publication.objects.get_or_create(
            document_id=document_id,
            defaults={"submitter": request.user, "status": "unsubmitted"},
        )
    else:
        publication = models.Publication.objects.filter(
            document_id=document_id,
        ).first()
        if not publication:
            # Access forbidden
            return HttpResponse("Missing access rights", status=403)
    message = {
        "type": "review",
        "message": request.POST.get("message"),
        "user": request.user.readable_name,
        "time": time.time(),
    }
    publication.messages.append(message)
    publication.save()
    response["message"] = message
    if document.owner != request.user:
        emails.send_review_notification(
            document.title,
            HttpRequest.build_absolute_uri(
                request, document.get_absolute_url()
            ),
            request.POST.get("message"),
            document.owner.readable_name,
            document.owner.email,
        )
    return JsonResponse(response, status=status)


@login_required
@require_POST
def publish_doc(request):
    response = {}
    if not (
        request.user.has_perm("website.add_publication")
        or request.user.has_perm("website.change_publication")
        or models.Editor.objects.filter(user=request.user).first()
    ):
        # Access forbidden
        return HttpResponse("Missing access rights", status=403)
    document_id = int(request.POST.get("doc_id"))
    document = Document.objects.filter(id=document_id).first()
    if not document:
        return HttpResponse("Not found", status=404)
    if (
        document.owner != request.user
        and not AccessRight.objects.filter(
            document=document,
            user=request.user,
            rights="write",
        ).first()
    ):
        # Access forbidden
        return HttpResponse("Missing document access rights", status=403)
    if (
        request.user.has_perm("website.add_publication")
        or models.Editor.objects.filter(user=request.user).first()
    ):
        publication, created = models.Publication.objects.get_or_create(
            document_id=document_id,
            defaults={"submitter_id": request.user.id},
        )
    else:
        publication = models.Publication.objects.filter(
            document_id=document_id,
        )
        if not publication:
            # Access forbidden
            return HttpResponse("Missing access rights", status=403)
    publication.title = request.POST.get("title")
    publication.abstract = request.POST.get("abstract")
    publication.authors = request.POST.getlist("authors[]")
    publication.keywords = request.POST.getlist("keywords[]")
    # Delete all existing assets
    models.PublicationAsset.objects.filter(publication=publication).delete()
    html_zip = zipfile.ZipFile(request.FILES.get("html.zip"))
    body_html = html_zip.open("document.html").read().decode("utf-8")
    publication.html_src = body_html
    publication.status = "published"
    message = {
        "type": "publish",
        "message": request.POST.get("message"),
        "user": request.user.readable_name,
        "time": time.time(),
    }
    publication.messages.append(message)
    response["message"] = message
    publication.save()

    # Iterate over document files
    for filepath in html_zip.namelist():
        if (
            filepath.endswith("/")
            or filepath == "document.html"
            or filepath not in body_html
        ):
            continue
        file = ContentFile(
            html_zip.open(filepath).read(),
            name=filepath.split("/")[-1],
        )
        asset = models.PublicationAsset.objects.create(
            publication=publication,
            file=file,
            filepath=filepath,
        )
        body_html = body_html.replace(filepath, asset.file.url)

    # Save html with adjusted links to media files with publication.
    publication.html_output = body_html
    publication.save()

    response["status"] = publication.status
    status = 200
    if document.owner != request.user:
        emails.send_publish_notification(
            document.title,
            HttpRequest.build_absolute_uri(
                request, document.get_absolute_url()
            ),
            request.POST.get("message"),
            document.owner.readable_name,
            document.owner.email,
        )
    return JsonResponse(response, status=status)


def list_publications(request, per_page=False, page_number=1):
    publications = models.Publication.objects.filter(
        status="published",
    ).order_by(
        "-added",
    )
    response = {}
    if per_page:
        paginator = Paginator(publications, per_page)
        page = paginator.get_page(page_number)
        publications = page.object_list
        response["num_pages"] = paginator.num_pages

    response["publications"] = [
        {
            "title": pub.title,
            "abstract": pub.abstract,
            "keywords": pub.keywords,
            "authors": pub.authors,
            "id": pub.id,
            "doc_id": pub.document_id,
            "added": pub.added,
            "updated": pub.updated,
        }
        for pub in publications
    ]
    response["site_name"] = get_current_site(request).name
    return JsonResponse(response, status=200)


def get_publication(request, id):
    publication = models.Publication.objects.filter(id=id).first()
    response = {}
    if publication:
        response["title"] = publication.title
        response["content"] = publication.html_output

        document = publication.document
        if not request.user.is_anonymous and (
            document.owner == request.user
            or AccessRight.objects.filter(
                document=document,
                user=request.user,
            ).first()
        ):
            # Has access right
            response["can_edit"] = True
        else:
            response["can_edit"] = False
        response["doc_id"] = publication.document_id

    return JsonResponse(response, status=200)


def get_style(request):
    response = {}
    design = models.Design.objects.filter(
        site__id=get_current_site(request).id
    ).first()
    if design:
        response["style"] = design.style
    return JsonResponse(response, status=200)
