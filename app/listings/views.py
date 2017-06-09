from django.views.generic import ListView, DetailView

from .filters import ListingFilter
from .models import Listing


class ListingList(ListView):
    model = Listing
    sort_default = 'boat__name'
    sort_fields = ['boat__name', 'boat__length', 'price', 'year', 'title', 'location', '-boat__name', '-boat__length', '-year', '-title', '-location', '-price']

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        sort = self.request.GET.get('sort', self.sort_default)
        if sort in self.sort_fields:
            return qs.order_by(sort)
        return qs.order_by(self.sort_default)


    def get_context_data(self, **kwargs):
       context = super().get_context_data()
       context['filter'] = ListingFilter(self.request.GET, queryset=self.get_queryset())
       return context

class ListingDetail(DetailView):
    model = Listing
