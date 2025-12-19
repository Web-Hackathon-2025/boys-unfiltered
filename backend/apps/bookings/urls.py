from django.urls import path
from . import views

urlpatterns = [
    # Bookings
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/status/', views.BookingStatusUpdateView.as_view(), name='booking-status-update'),
    
    # User-specific bookings
    path('customer/bookings/', views.CustomerBookingsView.as_view(), name='customer-bookings'),
    path('provider/bookings/', views.ProviderBookingsView.as_view(), name='provider-bookings'),
    path('upcoming/', views.UpcomingBookingsView.as_view(), name='upcoming-bookings'),
    path('stats/', views.BookingStatsView.as_view(), name='booking-stats'),
    
    # Attachments
    path('bookings/<int:booking_id>/attachments/', views.BookingAttachmentsView.as_view(), name='booking-attachments'),
]