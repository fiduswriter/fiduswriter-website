from django.contrib import admin

from . import models


class PublicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Publication, PublicationAdmin)


class PublicationAssetAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.PublicationAsset, PublicationAssetAdmin)


class DesignAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Design, DesignAdmin)
