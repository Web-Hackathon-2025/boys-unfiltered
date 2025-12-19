from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime, timedelta

from .models import Notification, NotificationTemplate, UserNotificationPreference, SMSLog, EmailLog
from .serializers import (
    NotificationSerializer, NotificationCreateSerializer,
    NotificationTemplateSerializer, UserNotificationPreferenceSerializer,
    SMSLogSerializer, EmailLogSerializer, MarkAsReadSerializer,
    NotificationCountSerializer
)
from apps.users.permissions import IsAdmin

class NotificationListView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'channel', 'is_read']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MarkAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = MarkAsReadSerializer(data=request.data)
        if serializer.is_valid():
            notification_ids = serializer.validated_data['notification_ids']
            notifications = Notification.objects.filter(
                id__in=notification_ids,
                user=request.user
            )
            
            count = 0
            for notification in notifications:
                notification.mark_as_read()
                count += 1
            
            return Response({
                "success": True,
                "message": f"Marked {count} notifications as read",
                "marked_count": count
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkAllAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )
        
        count = notifications.count()
        for notification in notifications:
            notification.mark_as_read()
        
        return Response({
            "success": True,
            "message": f"Marked all {count} notifications as read",
            "marked_count": count
        })

class NotificationCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        total = Notification.objects.filter(user=request.user).count()
        unread = Notification.objects.filter(user=request.user, is_read=False).count()
        
        serializer = NotificationCountSerializer({
            'total': total,
            'unread': unread
        })
        return Response(serializer.data)

class UserNotificationPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = UserNotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preference, created = UserNotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preference

class NotificationTemplateListView(generics.ListCreateAPIView):
    queryset = NotificationTemplate.objects.filter(is_active=True)
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
class NotificationTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class SMSLogListView(generics.ListAPIView):
    queryset = SMSLog.objects.all()
    serializer_class = SMSLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'provider']
    search_fields = ['recipient', 'message']

class EmailLogListView(generics.ListAPIView):
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['recipient', 'subject']

class SendTestNotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def post(self, request):
        from django.utils import timezone
        
        notification = Notification.objects.create(
            user=request.user,
            notification_type='system',
            title='Test Notification',
            message='This is a test notification sent by the admin.',
            channel='in_app',
            priority=1
        )
        
        serializer = NotificationSerializer(notification)
        return Response({
            "success": True,
            "message": "Test notification sent successfully",
            "notification": serializer.data
        })