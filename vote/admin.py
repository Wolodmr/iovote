# vote/admin.py
from django.contrib import admin
from .models import Vote

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'created_at')  # Remove 'session'
    list_filter = ('created_at',)  # Update with valid fields

