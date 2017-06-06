from django.views.generic import DetailView
from .models import Boat


class BoatDetail(DetailView):
    model = Boat

# Create your views here.
