from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count

from .models import Review, ReviewImage, ReviewHelpful, ProviderReport
from .serializers import (
    ReviewSerializer, ReviewCreateSerializer,
    ReviewImageSerializer, ReviewHelpfulSerializer,
    ProviderReportSerializer
)
from apps.users.permissions import IsCustomer, IsServiceProvider, IsAdmin

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['provider', 'rating', 'is_verified', 'is_featured']
    ordering_fields = ['rating', 'helpful_count', 'created_at']
    
    def get_queryset(self):
        queryset = Review.objects.filter(is_approved=True)
        
        # Filter by provider
        provider_id = self.request.query_params.get('provider')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        
        return queryset

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsCustomer()]
        return [permissions.IsAuthenticated()]

class ReviewImagesView(generics.ListCreateAPIView):
    serializer_class = ReviewImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return ReviewImage.objects.filter(review_id=review_id)
    
    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = Review.objects.get(id=review_id)
        
        # Check if user is the reviewer
        if review.customer != self.request.user:
            raise permissions.PermissionDenied("You can only add images to your own reviews")
        
        serializer.save(review=review)

class ReviewHelpfulView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            
            # Check if user already voted
            existing_vote = ReviewHelpful.objects.filter(review=review, user=request.user).first()
            
            if existing_vote:
                # Toggle vote
                existing_vote.delete()
                review.helpful_count = max(0, review.helpful_count - 1)
                message = "Vote removed"
            else:
                # Add new vote
                ReviewHelpful.objects.create(review=review, user=request.user, is_helpful=True)
                review.helpful_count += 1
                message = "Marked as helpful"
            
            review.save()
            
            return Response({
                "message": message,
                "helpful_count": review.helpful_count
            })
        
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

class ProviderReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        provider_id = self.kwargs.get('provider_id')
        return Review.objects.filter(provider_id=provider_id, is_approved=True)

class ProviderReportCreateView(generics.CreateAPIView):
    serializer_class = ProviderReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

class ProviderReportListView(generics.ListAPIView):
    serializer_class = ProviderReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return ProviderReport.objects.all()

class ProviderReportDetailView(generics.RetrieveUpdateAPIView):
    queryset = ProviderReport.objects.all()
    serializer_class = ProviderReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def perform_update(self, serializer):
        if serializer.validated_data.get('status') == 'resolved':
            serializer.save(resolved_by=self.request.user, resolved_at=datetime.now())
        else:
            serializer.save()

class TopRatedProvidersView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        providers = ServiceProvider.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).filter(
            avg_rating__gte=4.0,
            review_count__gte=5,
            is_verified=True
        ).order_by('-avg_rating', '-review_count')[:10]
        
        from apps.providers.serializers import ServiceProviderSerializer
        serializer = ServiceProviderSerializer(providers, many=True)
        return Response(serializer.data)