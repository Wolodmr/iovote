# voting_sessions/admin.py
from django.contrib import admin
from django.contrib import messages
from django.contrib import admin
from .models import Session, Option

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session_start_time', 'session_end_time', 'get_status', 'id', 'uuid')
    def get_status(self, obj):
        return obj.status
    get_status.short_description = 'Status'
    
    list_filter = ('session_start_time', 'session_end_time')
    search_fields = ('title', 'description')
    actions = ['send_invites_action']
    exclude = ('voting_duration','email_sent')
    readonly_fields = ('get_status',)
    
if not admin.site.is_registered(Session):
    admin.site.register(Session, SessionAdmin)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session')
    search_fields = ('title',)
    list_filter = ('session',)
