from django.urls import path
from . import views

urlpatterns = [
    # Notifications
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<uuid:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('mark-read/', views.MarkAsReadView.as_view(), name='mark-read'),
    path('mark-all-read/', views.MarkAllAsReadView.as_view(), name='mark-all-read'),
    path('count/', views.NotificationCountView.as_view(), name='notification-count'),
    
    # User Preferences
    path('preferences/', views.UserNotificationPreferenceView.as_view(), name='notification-preferences'),
    
    # Admin Endpoints
    path('templates/', views.NotificationTemplateListView.as_view(), name='notification-template-list'),
    path('templates/<uuid:pk>/', views.NotificationTemplateDetailView.as_view(), name='notification-template-detail'),
    path('sms-logs/', views.SMSLogListView.as_view(), name='sms-log-list'),
    path('email-logs/', views.EmailLogListView.as_view(), name='email-log-list'),
    path('send-test/', views.SendTestNotificationView.as_view(), name='send-test-notification'),
]