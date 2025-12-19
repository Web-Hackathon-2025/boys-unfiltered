from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App APIs
    path('api/users/', include('apps.users.urls')),
    path('api/services/', include('apps.services.urls')),
    path('api/providers/', include('apps.providers.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/payments/', include('apps.payments.urls')),
]