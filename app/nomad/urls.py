from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from listings.views import ListingList, ListingDetail
from boats.views import BoatDetail

admin.site.site_header = "Boats"
admin.site.site_title = "Boats"

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('listings/<int:pk>/', ListingDetail.as_view(), name="listing_detail"),
    path('', ListingList.as_view(), name="listing_list"),
    # path('boats/<int:pk>/', BoatDetail.as_view(), name="boat-detail"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
