from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count

from .models import ServiceProvider, ProviderDocument, ProviderAvailability
from .serializers import (
    ServiceProviderSerializer, ServiceProviderCreateSerializer,
    ProviderProfileUpdateSerializer, ProviderDocumentSerializer,
    ProviderAvailabilitySerializer
)
from apps.services.serializers import ServiceSerializer
from apps.users.permissions import IsServiceProvider, IsOwnerOrReadOnly
from apps.services.models import Service

class ProviderListView(generics.ListAPIView):
    serializer_class = ServiceProviderSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['business_name', 'city', 'state', 'skills']
    ordering_fields = ['average_rating', 'total_jobs_completed', 'hourly_rate']
    
    def get_queryset(self):
        queryset = ServiceProvider.objects.filter(is_verified=True, is_available=True)
        
        # Filter by location
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Filter by service category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(service_categories__id=category_id)
        
        # Filter by rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
        
        # Filter by emergency service
        emergency = self.request.query_params.get('emergency')
        if emergency and emergency.lower() == 'true':
            queryset = queryset.filter(emergency_service=True)
        
        return queryset.distinct()

class ProviderDetailView(generics.RetrieveAPIView):
    queryset = ServiceProvider.objects.filter(is_verified=True)
    serializer_class = ServiceProviderSerializer
    permission_classes = [permissions.AllowAny]

class ProviderCreateView(generics.CreateAPIView):
    serializer_class = ServiceProviderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.role != 'provider':
            raise permissions.PermissionDenied("Only users with provider role can create provider profile")
        serializer.save()

class ProviderProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ServiceProviderSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]
    
    def get_object(self):
        return self.request.user.provider_profile

class ProviderProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProviderProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]
    
    def get_object(self):
        return self.request.user.provider_profile

class ProviderServicesView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]
    
    def get_queryset(self):
        return Service.objects.filter(provider=self.request.user.provider_profile)

class ProviderDocumentsView(generics.ListCreateAPIView):
    serializer_class = ProviderDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]
    
    def get_queryset(self):
        return ProviderDocument.objects.filter(provider=self.request.user.provider_profile)
    
    def perform_create(self, serializer):
        serializer.save(provider=self.request.user.provider_profile)

class ProviderAvailabilityView(generics.ListCreateAPIView):
    serializer_class = ProviderAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]
    
    def get_queryset(self):
        return ProviderAvailability.objects.filter(provider=self.request.user.provider_profile)
    
    def perform_create(self, serializer):
        serializer.save(provider=self.request.user.provider_profile)

class TopProvidersView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        providers = ServiceProvider.objects.filter(
            is_verified=True,
            average_rating__gte=4.0
        ).order_by('-average_rating', '-total_jobs_completed')[:10]
        
        serializer = ServiceProviderSerializer(providers, many=True)
        return Response(serializer.data)

class ProviderStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]
    
    def get(self, request):
        provider = request.user.provider_profile
        stats = {
            'total_services': provider.services.count(),
            'total_bookings': provider.bookings.count(),
            'active_bookings': provider.bookings.filter(status__in=['pending', 'confirmed', 'accepted', 'in_progress']).count(),
            'completed_bookings': provider.bookings.filter(status='completed').count(),
            'average_rating': provider.average_rating,
            'total_reviews': provider.total_reviews,
            'completion_rate': provider.completion_rate,
            'response_time_minutes': provider.response_time_minutes,
        }
        return Response(stats)