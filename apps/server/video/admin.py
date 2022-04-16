from django.contrib import admin

from . import models


@admin.register(models.Attempt)
class AttemptAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AttemptSet)
class AttemptSetAdmin(admin.ModelAdmin):
    pass
