from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import ServiceCategory, Service, ServicePackage, ServiceRequest
from .serializers import (
    ServiceCategorySerializer, ServiceSerializer,
    ServicePackageSerializer, ServiceRequestSerializer
)
from .filters import ServiceFilter
from apps.users.permissions import IsCustomer, IsServiceProvider

class ServiceCategoryListView(generics.ListAPIView):
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ServiceCategoryDetailView(generics.RetrieveAPIView):
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]

class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title', 'description', 'provider__business_name']
    ordering_fields = ['base_price', 'average_rating', 'created_at']
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_available=True)
        
        # Filter by location if provided
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(provider__city__iexact=city)
        
        # Filter by category if provided
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset

class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]

class ServiceCreateView(generics.CreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]
    
    def perform_create(self, serializer):
        serializer.save(provider=self.request.user.provider_profile)

class ServiceUpdateView(generics.UpdateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]
    
    def get_queryset(self):
        return Service.objects.filter(provider=self.request.user.provider_profile)

class ServicePackageListView(generics.ListAPIView):
    queryset = ServicePackage.objects.all()
    serializer_class = ServicePackageSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        service_id = self.request.query_params.get('service_id')
        if service_id:
            return ServicePackage.objects.filter(service_id=service_id)
        return super().get_queryset()

class ServiceRequestListView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return ServiceRequest.objects.filter(customer=user)
        elif user.role == 'provider':
            # Providers can see requests in their categories
            provider_categories = user.provider_profile.service_categories.all()
            return ServiceRequest.objects.filter(category__in=provider_categories)
        return ServiceRequest.objects.all()
    
    def perform_create(self, serializer):
        if self.request.user.role != 'customer':
            raise permissions.PermissionDenied("Only customers can create service requests")
        serializer.save(customer=self.request.user)

class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return ServiceRequest.objects.filter(customer=user)
        elif user.role == 'provider':
            provider_categories = user.provider_profile.service_categories.all()
            return ServiceRequest.objects.filter(category__in=provider_categories)
        return ServiceRequest.objects.all()