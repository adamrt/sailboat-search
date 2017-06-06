from datetime import date

from django.contrib import admin

from .models import Listing
from .filters import DecadeFilter, LengthFilter

class ListingAdmin(admin.ModelAdmin):
    list_display = ['boat', 'get_length', 'year', 'price', 'get_listing_url', 'location', 'review', 'status', 'title']

    list_filter = [LengthFilter, DecadeFilter, 'boat']
    search_fields = ['title', 'boat__name']

    def get_length(self, obj):
        return obj.boat.length
    get_length.admin_order_field  = 'boat__length'
    get_length.short_description = 'Length'

    def get_listing_url(self, obj):
        return '<a target="_blank" href="%s">YachtWorld</a>' % (obj.url)
    get_listing_url.allow_tags = True
    get_listing_url.short_description = 'Listing URL'

admin.site.register(Listing, ListingAdmin)
