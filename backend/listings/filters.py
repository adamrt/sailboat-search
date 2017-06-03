from django.contrib import admin
from django.utils.translation import gettext_lazy as _


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


class LengthFilter(admin.SimpleListFilter):
    title = "length"
    parameter_name = 'length'

    def lookups(self, request, model_admin):
        return (
            ('large', _('44+')),
            ('42', _('42-43')),
            ('40', _('40-41')),
            ('38', _('38-39')),
            ('36', _('36-37')),
            ('34', _('34-35')),
            ('32', _('32-33')),
            ('30', _('30-31')),
            ('28', _('28-29')),
            ('26', _('26-27')),
            ('24', _('24-25')),
            ('small', _('23-'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'large':
            return queryset.filter(boat__length__gte=44)
        if self.value() == '42':
            return queryset.filter(boat__length__gte=42, boat__length__lte=43)
        if self.value() == '40':
            return queryset.filter(boat__length__gte=40, boat__length__lte=41)
        if self.value() == '38':
            return queryset.filter(boat__length__gte=38, boat__length__lte=39)
        if self.value() == '36':
            return queryset.filter(boat__length__gte=36, boat__length__lte=37)
        if self.value() == '34':
            return queryset.filter(boat__length__gte=34, boat__length__lte=35)
        if self.value() == '32':
            return queryset.filter(boat__length__gte=32, boat__length__lte=33)
        if self.value() == '30':
            return queryset.filter(boat__length__gte=30, boat__length__lte=31)
        if self.value() == '28':
            return queryset.filter(boat__length__gte=28, boat__length__lte=29)
        if self.value() == '26':
            return queryset.filter(boat__length__gte=26, boat__length__lte=27)
        if self.value() == '24':
            return queryset.filter(boat__length__gte=24, boat__length__lte=25)
        if self.value() == 'small':
            return queryset.filter(boat__length__lte=23)
