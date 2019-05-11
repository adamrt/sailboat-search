from django.utils.translation import gettext_lazy as _
from django import forms
from django.db.models import Q

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

    PRICE_CHOICES = (
        ('150', _('150K')),
        ('100', _('100K')),
        ('75', _('75K')),
        ('50', _('50K')),
        ('20', _('20K'))
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
        ('25', _('25 and less'))
    )

    name = django_filters.ModelChoiceFilter(field_name='boat_id', label="Model", queryset=Boat.objects.all(), empty_label="All Boats")
    bluewater = django_filters.BooleanFilter(field_name='boat__bluewater', label="Bluewater", widget=forms.CheckboxInput(), method='filter_bluewater')
    location = django_filters.BooleanFilter(label="US Only", method='filter_location', widget=forms.CheckboxInput())

    length = django_filters.MultipleChoiceFilter(
        choices=LENGTH_CHOICES,
        method='filter_length',
        widget=forms.CheckboxSelectMultiple
    )

    decade = django_filters.MultipleChoiceFilter(
        choices=DECADE_CHOICES,
        method='filter_decade',
        widget=forms.CheckboxSelectMultiple
    )

    price = django_filters.MultipleChoiceFilter(
        choices=PRICE_CHOICES,
        method='filter_price',
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Listing
        fields = ['name', 'bluewater', 'decade', 'length']

    def filter_bluewater(self, queryset, name, value):
        if value:
            return queryset.filter(boat__bluewater=True)
        return queryset

    def filter_location(self, queryset, name, value):
        if value:
            return queryset.filter(location__icontains="USA")
        return queryset

    def filter_price(self, queryset, name, value):
        query = Q()
        for v in value:
            if v == '150':
                query = query | Q(price__lte=150000)
            if v == '100':
                query = query | Q(price__lte=100000)
            if v == '75':
                query = query | Q(price__lte=75000)
            if v == '50':
                query = query | Q(price__lte=50000)
            if v == '20':
                query = query | Q(price__lte=20000)
        return queryset.filter(query)

    def filter_decade(self, queryset, name, value):
        query = Q()

        for v in value:
            if v == 'old':
                query = query | Q(year__lte=1959)
            if v == '60s':
                query = query | Q(year__gte=1960, year__lte=1969)
            if v == '70s':
                query = query | Q(year__gte=1970, year__lte=1979)
            if v == '80s':
                query = query | Q(year__gte=1980, year__lte=1989)
            if v == 'new':
                query = query | Q(year__gte=1990)
        return queryset.filter(query)

    def filter_length(self, queryset, name, value):
        query = Q()
        for v in value:
            if v == 'large':
                query = query | Q(boat__length__gte=44)
            if v == '42':
                query = query | Q(boat__length__gte=42, boat__length__lte=43.9)
            if v == '40':
                query = query | Q(boat__length__gte=40, boat__length__lte=41.9)
            if v == '38':
                query = query | Q(boat__length__gte=38, boat__length__lte=39.9)
            if v == '36':
                query = query | Q(boat__length__gte=36, boat__length__lte=37.9)
            if v == '34':
                query = query | Q(boat__length__gte=34, boat__length__lte=35.9)
            if v == '32':
                query = query | Q(boat__length__gte=32, boat__length__lte=33.9)
            if v == '30':
                query = query | Q(boat__length__gte=30, boat__length__lte=31.9)
            if v == '28':
                query = query | Q(boat__length__gte=28, boat__length__lte=29.9)
            if v == '26':
                query = query | Q(boat__length__gte=26, boat__length__lte=27.9)
            if v == '25':
                query = query | Q(boat__length__lte=25.9)

        return queryset.filter(query)
