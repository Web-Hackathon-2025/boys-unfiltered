from rest_framework import permissions

class IsBookingOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user

class IsBookingProvider(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'provider_profile') and obj.provider == request.user.provider_profile