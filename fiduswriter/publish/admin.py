from django.contrib import admin

from . import models


class PublicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Publication, PublicationAdmin)


class EditorAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Editor, EditorAdmin)
