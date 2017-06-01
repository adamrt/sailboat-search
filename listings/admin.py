from datetime import date

from django.contrib import admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Listing


class DecadeFilter(admin.SimpleListFilter):
    title = "decade born"
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        return (
            ('new', _('90s+')),
            ('80s', _('80s')),
            ('70s', _('70s')),
            ('60s', _('60s')),
            ('old', _('50s-')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'old':
            return queryset.filter(year__lte=1959)
        if self.value() == '60s':
            return queryset.filter(year__gte=1960, year__lte=1969)
        if self.value() == '70s':
            return queryset.filter(year__gte=1970, year__lte=1979)
        if self.value() == '80s':
            return queryset.filter(year__gte=1980, year__lte=1989)
        if self.value() == 'new':
            return queryset.filter(year__gte=1990)


class ListingAdmin(admin.ModelAdmin):
    list_display = ['name', 'boat', 'year', 'price', 'get_length', 'review']
    list_filter = ['review', DecadeFilter, 'boat']

    def get_length(self, obj):
        return obj.boat.length
    get_length.admin_order_field  = 'boat__length'
    get_length.short_description = 'Length'
admin.site.register(Listing, ListingAdmin)
