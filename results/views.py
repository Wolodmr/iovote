#results/views.py

from django.shortcuts import render, get_object_or_404
from voting_sessions.models import Session
from vote.models import Vote

def results_list(request, session_id):
    """Displays a summary of votes for a session."""
    session = get_object_or_404(Session, id=session_id)
    votes = Vote.objects.filter(session=session)
    summary = {}
    for vote in votes:
        summary[vote.option] = summary.get(vote.option, 0) + 1
    return render(request, "results/results_list.html", {"session": session, "summary": summary})

def results_detail(request, session_id):
    """Displays detailed information about a specific session's results."""
    session = get_object_or_404(Session, id=session_id)
    votes = Vote.objects.filter(session=session)
    return render(request, "results/results_detail.html", {"session": session, "votes": votes})

