# admin.py

from django.contrib import admin
from .models import VotingSession, VotingOption, Vote, Reader, Participation

class VotingSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'is_started', 'display_voting_options', 'voting_preference', 'duration', 'start_date' )
    fields = ('is_active', 'is_started', 'display_voting_options', 'duration', 'start_date')
    readonly_fields = ('display_voting_options',)  # Make it read-only as it’s an aggregate of related objects

admin.site.register(VotingSession, VotingSessionAdmin)
admin.site.register(VotingOption)
admin.site.register(Vote)
admin.site.register(Reader)
admin.site.register(Participation)
