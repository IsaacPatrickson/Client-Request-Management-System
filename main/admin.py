from django.contrib import admin
from .models import Client, RequestType, ClientRequest
from django.utils.html import format_html


# Inlines
class ClientRequestInline(admin.TabularInline):
    model = ClientRequest
    extra = 1
    fields = ('request_type', 'status', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True
    
    

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'contact_number', 'company_url', 'created_at', 'is_active')
    search_fields = ('name', 'email', 'contact_number', 'company_url')
    list_filter = ('created_at', 'is_active')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'contact_number', 'company_url', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def is_active_colour(self, obj):
        color = 'green' if obj.is_active else 'red'
        status = 'Active' if obj.is_active else 'Inactive'
        return format_html('<span style="color: {};">{}</span>', color, status)
    is_active_colour.short_description = 'Status'


@admin.register(RequestType)
class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    
    fieldsets = (
        (None, {
            'fields': ('id', 'name')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
    )


@admin.register(ClientRequest)
class ClientRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'request_type', 'status', 'description','created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__name', 'request_type__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('client', 'request_type', 'status')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        updated_count = queryset.update(status='Completed')
        self.message_user(request, f'{updated_count} requests marked as completed.')
    mark_as_completed.short_description = 'Mark selected requests as completed'
