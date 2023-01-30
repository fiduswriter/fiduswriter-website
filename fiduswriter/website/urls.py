from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        "^get_doc_info/$",
        views.get_doc_info,
        name="website_get_doc_info",
    ),
    re_path("^submit_doc/$", views.submit_doc, name="website_submit_doc"),
    re_path("^reject_doc/$", views.reject_doc, name="website_reject_doc"),
    re_path("^review_doc/$", views.review_doc, name="website_review_doc"),
    re_path("^publish_doc/$", views.publish_doc, name="website_publish_doc"),
    re_path(
        "^list_publications/$",
        views.list_publications,
        name="website_list_publications",
    ),
    re_path(
        "^list_publications/(?P<per_page>[0-9]+)/(?P<page_number>[0-9]+)/$",
        views.list_publications,
        name="website_list_publications",
    ),
    re_path(
        "^get_publication/(?P<id>[0-9]+)/$",
        views.get_publication,
        name="website_get_publication",
    ),
    re_path(
        "^get_style/$",
        views.get_style,
        name="website_get_style",
    ),
]
