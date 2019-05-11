from django.contrib import admin

from .models import Boat


class BoatAdmin(admin.ModelAdmin):
    list_display = ["name", "display_length", "slug"]


admin.site.register(Boat, BoatAdmin)
