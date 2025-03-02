from django.urls import path
from .views import (
    TourListCreateView, TourDetailView, tour_list_html, tour_list_json,
    BookingListCreateView, UserBookingsView, AdminBookingListView
)

urlpatterns = [
    # ✅ **Frontend üçün HTML görünüşü**
    path('html/', tour_list_html, name='tour_list_html'),

    # ✅ **JSON qaytaran API**
    path('json/', tour_list_json, name='tour_list_json'),

    # ✅ **Tur API-ləri** (artıq `tours/` prefix-i yoxdur!)
    path('', TourListCreateView.as_view(), name='tour-list-create'),
    path('<int:pk>/', TourDetailView.as_view(), name='tour-detail'),

    # ✅ **Rezervasiya API-ləri** (artıq `tours/` prefix-i yoxdur!)
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/my/', UserBookingsView.as_view(), name='user-bookings'),
    path('bookings/admin/', AdminBookingListView.as_view(), name='admin-bookings'),
]
