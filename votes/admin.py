from django.contrib import admin
from .models import VotingSession, Vote, VotingOption, Reader, Participation

admin.site.register(VotingSession)
admin.site.register(Vote)
admin.site.register(VotingOption)
admin.site.register(Reader)
admin.site.register(Participation)