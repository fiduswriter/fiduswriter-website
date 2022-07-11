from django.conf.urls import url

from . import views

urlpatterns = [
    url("^get_doc_info/$", views.get_doc_info, name="publish_get_doc_info"),
    url("^submit_doc/$", views.submit_doc, name="publish_submit_doc"),
    url("^reject_doc/$", views.reject_doc, name="publish_reject_doc"),
    url("^review_doc/$", views.review_doc, name="publish_review_doc"),
    url("^publish_doc/$", views.publish_doc, name="publish_publish_doc"),
    url(
        "^list_publications/$",
        views.list_publications,
        name="publish_list_publications",
    ),
    url(
        "^get_publication/(?P<id>[0-9]+)/$",
        views.get_publication,
        name="publish_get_publication",
    ),
]
