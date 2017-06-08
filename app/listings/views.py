from django.views.generic import ListView, DetailView

from .models import Listing


class ListingList(ListView):
    model = Listing
    sort_default = 'boat__name'
    sort_fields = ['boat__name', 'boat__length', 'year', 'title', 'location', '-boat__name', '-boat__length', '-year', '-title', '-location']

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        sort = self.request.GET.get('sort', self.sort_default)
        if sort in self.sort_fields:
            self.sort = sort
        return qs.order_by(self.sort)

class ListingDetail(DetailView):
    model = Listing
