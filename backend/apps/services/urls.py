from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.ServiceCategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.ServiceCategoryDetailView.as_view(), name='category-detail'),
    
    # Services
    path('services/', views.ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service-update'),
    
    # Service Packages
    path('packages/', views.ServicePackageListView.as_view(), name='package-list'),
    
    # Service Requests
    path('requests/', views.ServiceRequestListView.as_view(), name='request-list'),
    path('requests/<int:pk>/', views.ServiceRequestDetailView.as_view(), name='request-detail'),
]