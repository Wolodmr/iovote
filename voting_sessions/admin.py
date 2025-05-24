# voting_sessions/admin.py
from django.contrib import admin
from django.contrib import messages
from django.contrib import admin
from .models import Session, Option

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session_start_time', 'session_end_time', 'is_active', 'email_sent', 'id', 'uuid')
    list_filter = ('session_start_time', 'session_end_time')
    search_fields = ('title', 'description')
    actions = ['send_invites_action']
    exclude = ('voting_duration',)
    
    def send_invites_action(self, request, queryset):
        """Admin action to send invitations."""
        for session in queryset:
            if not session.email_sent:
                session.send_invites()
                self.message_user(request, f"Invitations sent for session: {session.title}", messages.SUCCESS)
            else:
                self.message_user(request, f"Invitations were already sent for: {session.title}", messages.WARNING)
    send_invites_action.short_description = "Send Email Invitations"
#admin.site.register(Session, SessionAdmin)
if not admin.site.is_registered(Session):
    admin.site.register(Session, SessionAdmin)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session')
    search_fields = ('title',)
    list_filter = ('session',)
