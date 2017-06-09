from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django import forms

import django_filters
from .models import Listing
from boats.models import Boat

class ListingFilter(django_filters.FilterSet):
    DECADE_CHOICES = (
        ('new', _('90s and newer')),
        ('80s', _('80s')),
        ('70s', _('70s')),
        ('60s', _('60s')),
        ('old', _('50s and older')),
    )
    LENGTH_CHOICES = (
        ('large', _('44 and more')),
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
        ('small', _('23 and less'))
    )

    name = django_filters.ModelChoiceFilter(name='boat_id', label="Model", queryset=Boat.objects.all(), empty_label="All Boats")
    decade = django_filters.ChoiceFilter(choices=DECADE_CHOICES, method='filter_decade', widget=django_filters.widgets.LinkWidget())
    length = django_filters.ChoiceFilter(choices=LENGTH_CHOICES, method='filter_length', widget=django_filters.widgets.LinkWidget())

    class Meta:
        model = Listing
        fields = ['name', 'decade', 'length']


    def filter_decade(self, queryset, name, value):
        if value == 'old':
            return queryset.filter(year__lte=1959)
        if value == '60s':
            return queryset.filter(year__gte=1960, year__lte=1969)
        if value == '70s':
            return queryset.filter(year__gte=1970, year__lte=1979)
        if value == '80s':
            return queryset.filter(year__gte=1980, year__lte=1989)
        if value == 'new':
            return queryset.filter(year__gte=1990)

    def filter_length(self, queryset, name, value):
        if value == 'large':
            return queryset.filter(boat__length__gte=44)
        if value == '42':
            return queryset.filter(boat__length__gte=42, boat__length__lte=43)
        if value == '40':
            return queryset.filter(boat__length__gte=40, boat__length__lte=41)
        if value == '38':
            return queryset.filter(boat__length__gte=38, boat__length__lte=39)
        if value == '36':
            return queryset.filter(boat__length__gte=36, boat__length__lte=37)
        if value == '34':
            return queryset.filter(boat__length__gte=34, boat__length__lte=35)
        if value == '32':
            return queryset.filter(boat__length__gte=32, boat__length__lte=33)
        if value == '30':
            return queryset.filter(boat__length__gte=30, boat__length__lte=31)
        if value == '28':
            return queryset.filter(boat__length__gte=28, boat__length__lte=29)
        if value == '26':
            return queryset.filter(boat__length__gte=26, boat__length__lte=27)
        if value == '24':
            return queryset.filter(boat__length__gte=24, boat__length__lte=25)
        if value == 'small':
            return queryset.filter(boat__length__lte=23)
