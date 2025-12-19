from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime, timedelta

from .models import Booking, BookingStatusHistory, BookingAttachment
from .serializers import (
    BookingSerializer, BookingCreateSerializer,
    BookingUpdateSerializer, BookingAttachmentSerializer,
    BookingStatusHistorySerializer
)
from apps.users.permissions import IsCustomer, IsServiceProvider
from .permissions import IsBookingOwner, IsBookingProvider


class BookingListView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'priority']
    search_fields = ['booking_number', 'problem_description', 'service_address']
    ordering_fields = ['scheduled_date', 'created_at', 'quoted_price']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Booking.objects.filter(customer=user)
        elif user.role == 'provider':
            return Booking.objects.filter(provider=user.provider_profile)
        return Booking.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingSerializer
    
    def perform_create(self, serializer):
        if self.request.user.role != 'customer':
            raise permissions.PermissionDenied("Only customers can create bookings")
        serializer.save(customer=self.request.user)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Booking.objects.filter(customer=user)
        elif user.role == 'provider':
            return Booking.objects.filter(provider=user.provider_profile)
        return Booking.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BookingUpdateSerializer
        return BookingSerializer


class CustomerBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)


class ProviderBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]
    
    def get_queryset(self):
        return Booking.objects.filter(provider=self.request.user.provider_profile)


class BookingStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookingProvider]
    
    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            new_status = request.data.get('status')
            
            if not new_status:
                return Response({"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            if new_status not in dict(booking.Status.choices):
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create status history
            BookingStatusHistory.objects.create(
                booking=booking,
                old_status=booking.status,
                new_status=new_status,
                changed_by=request.user,
                notes=request.data.get('notes', '')
            )
            
            # Update booking status
            booking.status = new_status
            
            # Update timestamps based on status
            now = datetime.now()
            if new_status == 'accepted':
                booking.assigned_at = now
            elif new_status == 'in_progress':
                booking.started_at = now
            elif new_status == 'completed':
                booking.completed_at = now
            elif new_status == 'cancelled':
                booking.cancelled_at = now
                booking.cancellation_reason = request.data.get('cancellation_reason', '')
            
            booking.save()
            
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


class BookingAttachmentsView(generics.ListCreateAPIView):
    serializer_class = BookingAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        booking_id = self.kwargs.get('booking_id')
        return BookingAttachment.objects.filter(booking_id=booking_id)
    
    def perform_create(self, serializer):
        booking_id = self.kwargs.get('booking_id')
        booking = Booking.objects.get(id=booking_id)
        
        # Check permissions
        user = self.request.user
        if not (user == booking.customer or 
                (hasattr(user, 'provider_profile') and user.provider_profile == booking.provider)):
            raise permissions.PermissionDenied("You don't have permission to add attachments to this booking")
        
        serializer.save(booking=booking, uploaded_by=user)


class UpcomingBookingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        today = datetime.now().date()
        
        if user.role == 'customer':
            bookings = Booking.objects.filter(
                customer=user,
                scheduled_date__gte=today,
                status__in=['pending', 'confirmed', 'accepted']
            ).order_by('scheduled_date', 'scheduled_time')
        elif user.role == 'provider':
            bookings = Booking.objects.filter(
                provider=user.provider_profile,
                scheduled_date__gte=today,
                status__in=['pending', 'confirmed', 'accepted']
            ).order_by('scheduled_date', 'scheduled_time')
        else:
            bookings = Booking.objects.none()
        
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class BookingStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.role == 'customer':
            bookings = Booking.objects.filter(customer=user)
        elif user.role == 'provider':
            bookings = Booking.objects.filter(provider=user.provider_profile)
        else:
            bookings = Booking.objects.none()
        
        stats = {
            'total': bookings.count(),
            'pending': bookings.filter(status='pending').count(),
            'confirmed': bookings.filter(status='confirmed').count(),
            'accepted': bookings.filter(status='accepted').count(),
            'in_progress': bookings.filter(status='in_progress').count(),
            'completed': bookings.filter(status='completed').count(),
            'cancelled': bookings.filter(status='cancelled').count(),
        }
        
        # Monthly stats for the last 6 months
        monthly_stats = []
        for i in range(5, -1, -1):
            month = datetime.now().date().replace(day=1) - timedelta(days=30*i)
            month_bookings = bookings.filter(created_at__year=month.year, created_at__month=month.month)
            monthly_stats.append({
                'month': month.strftime('%b %Y'),
                'count': month_bookings.count(),
                'revenue': sum(b.total_amount for b in month_bookings if b.total_amount)
            })
        
        stats['monthly_stats'] = monthly_stats
        
        return Response(stats)