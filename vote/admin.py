# vote/admin.py
from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Vote model.

    Displays user, option, and creation date in the admin panel.
    Allows filtering by creation date.
    """
    list_display = ('user', 'option', 'created_at')
    list_filter = ('created_at',)


