from django.conf.urls import url

from . import views

urlpatterns = [
    url("^get_doc_info/$", views.get_doc_info, name="publish_get_doc_info"),
    url("^submit_doc/$", views.submit_doc, name="publish_submit_doc"),
]
