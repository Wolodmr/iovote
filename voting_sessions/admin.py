# voting_sessions/admin.py
from django.contrib import admin
from .models import Session, Option

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session_start_time', 'session_end_time')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session')
