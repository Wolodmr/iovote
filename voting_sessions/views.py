from django.shortcuts import render, get_object_or_404
from .models import Session, Option
from django.views.generic import DetailView
from django.http import HttpResponse
from django.views import View
from voting_sessions.models import Session
from .models import Option
from django.http import HttpResponse

def vote(request, session_id):
    return HttpResponse(f"Voting page for session {session_id}")

class VoteView(View):
    def post(self, request, session_id):
        session = get_object_or_404(Session, id=session_id)
        # Placeholder logic: Process the vote and ensure the user votes only once
        return HttpResponse(f"Vote recorded for session {session.title}")


def session_list(request):
    """List all current and closed sessions."""
    sessions = Session.objects.all().order_by("-session_start_time")
    return render(request, "voting_sessions/session_list.html", {"sessions": sessions})

def session_detail(request, session_id):
    """View details of a specific session."""
    session = get_object_or_404(Session, id=session_id)
    return render(request, "voting_sessions/session_detail.html", {"session": session})

class SessionDetailView(DetailView):
    model = Session
    template_name = "voting_sessions/session_detail.html"
    context_object_name = "session"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add voting options to the context
        context["options"] = Option.objects.filter(session=self.object)
        return context
