from django.contrib import admin

from .models import Boat


class BoatAdmin(admin.ModelAdmin):
    list_display = ['name', 'length', 'slug']
    list_editable = ['length']
admin.site.register(Boat, BoatAdmin)
