"""Services admin configuration."""

from django.contrib import admin
from .models import ServiceCategory, Service, ServiceFeature, ServiceLead


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 3


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'level', 'is_featured', 'is_popular', 'is_active', 'order')
    list_filter = ('category', 'level', 'is_featured', 'is_popular', 'is_active')
    list_editable = ('price', 'is_featured', 'is_popular', 'is_active', 'order')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceFeatureInline]


@admin.register(ServiceLead)
class ServiceLeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'service', 'is_contacted', 'created_at')
    list_filter = ('is_contacted', 'created_at')
    list_editable = ('is_contacted',)
    search_fields = ('full_name', 'phone', 'description')
    readonly_fields = ('created_at',)
