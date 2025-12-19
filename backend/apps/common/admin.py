from django.contrib import admin
from .models import BaseModel

# Base admin class for models inheriting from BaseModel
class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

# Since BaseModel is abstract, we don't register it
# This file can be used as a base for other admin classes