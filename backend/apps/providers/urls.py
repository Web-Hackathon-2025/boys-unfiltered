from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('providers/', views.ProviderListView.as_view(), name='provider-list'),
    path('providers/<int:pk>/', views.ProviderDetailView.as_view(), name='provider-detail'),
    path('providers/top/', views.TopProvidersView.as_view(), name='top-providers'),
    
    # Provider registration
    path('providers/register/', views.ProviderCreateView.as_view(), name='provider-create'),
    
    # Provider profile management
    path('profile/', views.ProviderProfileView.as_view(), name='provider-profile'),
    path('profile/update/', views.ProviderProfileUpdateView.as_view(), name='provider-profile-update'),
    path('profile/services/', views.ProviderServicesView.as_view(), name='provider-services'),
    path('profile/documents/', views.ProviderDocumentsView.as_view(), name='provider-documents'),
    path('profile/availability/', views.ProviderAvailabilityView.as_view(), name='provider-availability'),
    path('profile/stats/', views.ProviderStatsView.as_view(), name='provider-stats'),
]