# results/views.py
from django.shortcuts import render, get_object_or_404
from voting_sessions.models import Session
from vote.models import Vote
from django.db.models import Count

def results_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    # Filter votes related to the session through the option's session
    votes = Vote.objects.filter(option__session=session)
    # Aggregate vote counts per option
    vote_counts = votes.values('option__title').annotate(count=Count('id'))
    return render(request, 'results/results_detail.html', {
        'session': session,
        'vote_counts': vote_counts,
    })
    
def results_list(request):
    sessions = Session.objects.all()
    return render(request, 'results/results_list.html', {'sessions': sessions})
