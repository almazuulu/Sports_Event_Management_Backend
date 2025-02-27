# admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Event, SportEvent


class SportEventInline(admin.TabularInline):
    model = SportEvent
    extra = 0
    fields = ['name', 'sport_type', 'start_date', 'end_date', 'status']
    

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'location', 'status', 'created_by']
    list_filter = ['status', 'start_date', 'location']
    search_fields = ['name', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    date_hierarchy = 'start_date'
    inlines = [SportEventInline]
    
    fieldsets = (
        (None, {'fields': ('name', 'description', 'location')}),
        (_('Date information'), {'fields': ('start_date', 'end_date')}),
        (_('Status'), {'fields': ('status',)}),
        (_('Metadata'), {'fields': ('created_by', 'created_at', 'updated_by', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        # Only admins can add events
        return request.user.role == 'admin'
    
    def has_change_permission(self, request, obj=None):
        # Only admins can change events
        return request.user.role == 'admin'
    
    def has_delete_permission(self, request, obj=None):
        # Only admins can delete events
        return request.user.role == 'admin'


@admin.register(SportEvent)
class SportEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'sport_type', 'start_date', 'end_date', 'status', 'registration_deadline']
    list_filter = ['sport_type', 'status', 'start_date']
    search_fields = ['name', 'description', 'rules', 'scoring_system']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        (None, {'fields': ('event', 'name', 'description', 'sport_type')}),
        (_('Date information'), {'fields': ('start_date', 'end_date', 'registration_deadline')}),
        (_('Settings'), {'fields': ('max_teams', 'status')}),
        (_('Rules and scoring'), {'fields': ('rules', 'scoring_system')}),
        (_('Metadata'), {'fields': ('created_by', 'created_at', 'updated_by', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        # Only admins can add sport events
        return request.user.role == 'admin'
    
    def has_change_permission(self, request, obj=None):
        # Only admins can change sport events
        return request.user.role == 'admin'
    
    def has_delete_permission(self, request, obj=None):
        # Only admins can delete sport events
        return request.user.role == 'admin'