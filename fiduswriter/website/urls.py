from django.conf.urls import url

from . import views

urlpatterns = [
    url("^get_doc_info/$", views.get_doc_info, name="website_get_doc_info"),
    url("^submit_doc/$", views.submit_doc, name="website_submit_doc"),
    url("^reject_doc/$", views.reject_doc, name="website_reject_doc"),
    url("^review_doc/$", views.review_doc, name="website_review_doc"),
    url("^publish_doc/$", views.publish_doc, name="website_publish_doc"),
    url(
        "^list_publications/$",
        views.list_publications,
        name="website_list_publications",
    ),
    url(
        "^get_publication/(?P<id>[0-9]+)/$",
        views.get_publication,
        name="website_get_publication",
    ),
]
