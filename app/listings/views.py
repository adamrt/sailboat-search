from django.views.generic import ListView, DetailView

from .models import Listing


class ListingList(ListView):
    model = Listing

class ListingDetail(DetailView):
    model = Listing
